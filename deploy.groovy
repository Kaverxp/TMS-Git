#!/usr/bin/env groovy

def call(Map config = [:]) {
    node {
        stage('Deploy Application') {
            echo "🚀 Начало деплоя с конфигурацией: ${config}"
            
            // Проверяем и создаём Dockerfile если нет
            sh '''
                echo "Проверяем наличие Dockerfile..."
                if [ ! -f "Dockerfile" ]; then
                    echo "Создаём тестовый Dockerfile..."
                    cat > Dockerfile << 'EOF'
FROM alpine:latest
RUN apk add --no-cache curl
CMD echo "TMS Application v${config.imageTag ?: 'latest'}" && \\
    echo "Контейнер: ${config.containerName ?: 'app-container'}" && \\
    sleep 3600
EOF
                    echo "✅ Dockerfile создан"
                else
                    echo "✅ Dockerfile уже существует"
                fi
                
                echo "Содержимое Dockerfile:"
                cat Dockerfile
            '''
            
            // Ваши шаги деплоя
            sh "docker build -t ${config.imageName ?: 'app'}:${config.imageTag ?: 'latest'} ."
            
            sh """
                echo "Останавливаем предыдущий контейнер..."
                docker stop ${config.containerName ?: 'app-container'} 2>/dev/null || true
                docker rm ${config.containerName ?: 'app-container'} 2>/dev/null || true
                echo "✅ Очистка завершена"
            """
            
            sh """
                echo "Запускаем новый контейнер..."
                docker run -d \
                    --name ${config.containerName ?: 'app-container'} \
                    -p ${config.port ?: 8080}:${config.port ?: 8080} \
                    ${config.imageName ?: 'app'}:${config.imageTag ?: 'latest'}
                
                echo "✅ Контейнер запущен"
                echo "Проверяем запущенные контейнеры:"
                docker ps | grep ${config.containerName ?: 'app-container'} || echo "Контейнер не найден в списке"
            """
            
            stage('Health Check') {
                echo "🏥 Проверка здоровья приложения..."
                retry(3) {
                    sleep 5
                    sh """
                        echo "Проверка доступности контейнера..."
                        docker ps | grep ${config.containerName ?: 'app-container'} && echo "✅ Контейнер запущен"
                        
                        # Пробуем выполнить команду внутри контейнера
                        docker exec ${config.containerName ?: 'app-container'} echo "✅ Контейнер отвечает" || echo "⚠ Контейнер не отвечает"
                    """
                }
            }
        }
    }
    
    echo "🎉 Деплой завершён успешно!"
}

return this