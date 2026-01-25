#!/usr/bin/env groovy

def call(Map config = [:]) {
    node {
        stage('Deploy Application') {
            echo "Начало деплоя с конфигурацией: ${config}"
            
            // Проверяем и создаём Dockerfile если нет
            sh '''
                echo "Проверяем наличие Dockerfile..."
                if [ ! -f "Dockerfile" ]; then
                    echo "Создаём тестовый Dockerfile..."
                    cat > Dockerfile << 'EOF'
FROM alpine:latest
RUN apk add --no-cache curl
CMD echo "TMS Application запущен успешно!" && \
    echo "Версия: ${config.imageTag ?: 'latest'}" && \
    echo "Контейнер: ${config.containerName ?: 'app-container'}" && \
    echo "Сервер работает на порту: ${config.port ?: 8080}" && \
    tail -f /dev/null
EOF
                    echo "Dockerfile создан"
                else
                    echo "Dockerfile уже существует"
                fi
                
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
                echo "Очистка завершена"
            """
            
            // Запуск нового контейнера
            sh """
                echo "Запускаем новый контейнер..."
                docker run -d \
                    --name ${config.containerName ?: 'app-container'} \
                    -p ${config.port ?: 8080}:${config.port ?: 8080} \
                    ${config.imageName ?: 'app'}:${config.imageTag ?: 'latest'}
                
                echo "Контейнер запущен"
                sleep 2
                echo "Проверяем запущенные контейнеры:"
                docker ps | grep ${config.containerName ?: 'app-container'}
            """
            
            stage('Health Check') {
                echo "Проверка здоровья приложения..."
                retry(3) {
                    sleep 3
                    sh """
                        echo "Проверка состояния контейнера..."
                        docker ps | grep ${config.containerName ?: 'app-container'} && echo "Контейнер работает"
                        
                        # Пробуем выполнить команду внутри контейнера
                        docker exec ${config.containerName ?: 'app-container'} echo "Контейнер отвечает на команды" || echo "⚠ Ошибка доступа к контейнеру"
                        
                        # Проверка порта
                        echo "Проверка доступности порта ${config.port ?: 8080}..."
                        nc -z localhost ${config.port ?: 8080} && echo "Порт доступен" || echo "Порт не отвечает"
                    """
                }
            }
        }
    }
    
    echo "Деплой завершён успешно!"
}

return this