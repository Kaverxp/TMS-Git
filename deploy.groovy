#!/usr/bin/env groovy

def call(Map config = [:]) {
    node {
        stage('Deploy Application') {
            echo "🚀 Начало деплоя с конфигурацией: ${config}"
            
            // Создаём Dockerfile
            sh '''
                echo "Создаём Dockerfile..."
                cat > Dockerfile << 'EOF'
FROM alpine:latest
RUN apk add --no-cache curl
CMD echo "TMS Application запущен" && \
    echo "Сервер работает..." && \
    tail -f /dev/null
EOF
                
                echo "✅ Dockerfile создан"
                cat Dockerfile
            '''
            
            // Сборка Docker образа
            sh "docker build -t ${config.imageName ?: 'app'}:${config.imageTag ?: 'latest'} ."
            
            // Очистка предыдущего контейнера
            sh """
                echo "Останавливаем предыдущий контейнер..."
                docker stop ${config.containerName ?: 'app-container'} 2>/dev/null || true
                docker rm ${config.containerName ?: 'app-container'} 2>/dev/null || true
                echo "✅ Очистка завершена"
            """
            
            // Запуск нового контейнера
            sh """
                echo "Запускаем новый контейнер..."
                docker run -d \\
                    --name ${config.containerName ?: 'app-container'} \\
                    -p ${config.port ?: 8080}:${config.port ?: 8080} \\
                    ${config.imageName ?: 'app'}:${config.imageTag ?: 'latest'}
                
                echo "✅ Контейнер запущен"
                sleep 2
                
                echo "Проверяем контейнеры:"
                docker ps | grep ${config.containerName ?: 'app-container'} || echo "Контейнер не найден в running состоянии"
            """
            
            stage('Health Check') {
                echo "🏥 Проверка здоровья приложения..."
                
                retry(3) {
                    sleep 2
                    sh """
                        echo "Проверка состояния контейнера..."
                        
                        # Проверяем статус контейнера
                        if docker ps | grep -q ${config.containerName ?: 'app-container'}; then
                            echo "✅ Контейнер запущен"
                            docker exec ${config.containerName ?: 'app-container'} echo "✅ Контейнер отвечает"
                        else
                            echo "⚠ Контейнер не запущен. Проверяем все контейнеры..."
                            docker ps -a | grep ${config.containerName ?: 'app-container'} || echo "Контейнер не найден"
                            exit 1
                        fi
                    """
                }
            }
        }
    }
    
    echo "🎉 Деплой завершён успешно!"
}

return this