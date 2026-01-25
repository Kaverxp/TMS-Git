#!/usr/bin/env groovy

def call(Map config = [:]) {
    node {
        stage('Deploy Application') {
            echo "🚀 Начало деплоя с конфигурацией: ${config}"
            
            // Создаём правильный Dockerfile (FIXED)
            sh """
                echo "Создаём Dockerfile..."
                cat > Dockerfile << 'EOF'
FROM alpine:latest
RUN apk add --no-cache curl
CMD echo "TMS Application v${config.imageTag ?: 'latest'} запущен" && \\
    echo "Имя контейнера: ${config.containerName ?: 'app-container'}" && \\
    echo "Порт: ${config.port ?: 8080}" && \\
    echo "Сервер работает..." && \\
    tail -f /dev/null
EOF
                
                echo "✅ Dockerfile создан"
                echo "Содержимое Dockerfile:"
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
                
                # Даём время на запуск
                sleep 3
                
                echo "Проверяем запущенные контейнеры:"
                docker ps | grep ${config.containerName ?: 'app-container'} || echo "⚠ Контейнер не найден в running состоянии"
                
                echo "Все контейнеры (включая остановленные):"
                docker ps -a | grep ${config.containerName ?: 'app-container'} || echo "Контейнер не существует"
            """
            
            stage('Health Check') {
                echo "🏥 Проверка здоровья приложения..."
                
                retry(3) {
                    sleep 2
                    sh """
                        echo "Проверка состояния контейнера..."
                        
                        # Проверяем, что контейнер существует и запущен
                        CONTAINER_STATUS=\$(docker ps -a --filter "name=${config.containerName ?: 'app-container'}" --format "{{.Status}}" 2>/dev/null || echo "not found")
                        echo "Статус контейнера: \${CONTAINER_STATUS}"
                        
                        if echo "\${CONTAINER_STATUS}" | grep -q "Up"; then
                            echo "✅ Контейнер запущен и работает"
                            
                            # Пробуем выполнить команду внутри контейнера
                            docker exec ${config.containerName ?: 'app-container'} echo "✅ Контейнер отвечает на команды"
                            
                        elif echo "\${CONTAINER_STATUS}" | grep -q "Exited"; then
                            echo "⚠ Контейнер завершился. Логи:"
                            docker logs ${config.containerName ?: 'app-container'} 2>/dev/null | tail -5 || echo "Логи недоступны"
                            exit 1
                            
                        else
                            echo "❌ Контейнер не найден"
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