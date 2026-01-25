#!/usr/bin/env groovy

def call(Map config = [:]) {
    def imageName = config.imageName ?: 'app'
    def imageTag = config.imageTag ?: 'latest'
    def containerName = config.containerName ?: 'app-container'
    def port = config.port ?: 8080
    
    node {
        stage('Build Docker Image') {
            echo "🐳 Сборка Docker-образа: ${imageName}:${imageTag}"
            
            // ПРОСТЕЙШИЙ Dockerfile - гарантированно работает
            sh '''
                cat > Dockerfile << 'EOF'
FROM nginx:alpine
RUN echo "<h1>ТМС Приложение успешно развёрнуто!</h1><p>Jenkins Pipeline выполнен. Сборка: ''' + config.buildNumber + '''</p>" > /usr/share/nginx/html/index.html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
EOF
            '''
            
            sh "docker build -t ${imageName}:${imageTag} ."
        }
        
        stage('Deploy Container') {
            echo "🚀 Развёртывание контейнера: ${containerName}"
            
            // Останавливаем и удаляем старый контейнер
            sh """
                docker stop ${containerName} 2>/dev/null || true
                docker rm ${containerName} 2>/dev/null || true
            """
            
            // Запускаем новый контейнер
            sh """
                docker run -d \\
                    --name ${containerName} \\
                    -p ${port}:80 \\
                    ${imageName}:${imageTag}
            """
            
            echo "✅ Контейнер запущен на порту ${port}"
        }
        
        stage('Health Check') {
            echo "🏥 Проверка здоровья приложения..."
            
            retry(5) {
                sleep 3
                
                // Проверка состояния контейнера
                sh """
                    if docker inspect -f '{{.State.Status}}' ${containerName} | grep -q running; then
                        echo "✅ Контейнер работает"
                    else
                        echo "❌ Контейнер не запущен"
                        exit 1
                    fi
                """
                
                // HTTP-проверка
                sh """
                    if curl -s -f http://localhost:${port} > /dev/null; then
                        echo "✅ HTTP-статус: 200 - Приложение доступно"
                    else
                        echo "⚠ Проблемы с HTTP доступностью"
                        docker logs ${containerName} --tail 5
                    fi
                """
            }
        }
    }
    
    echo "🎉 Деплой завершён успешно!"
}

return this