#!/usr/bin/env groovy

def call(Map config = [:]) {
    def imageName = config.imageName ?: 'app'
    def imageTag = config.imageTag ?: 'latest'
    def containerName = config.containerName ?: 'app-container'
    def port = config.port ?: 8080
    def appUrl = config.appUrl ?: "http://localhost:${port}"
    
    node {
        stage('Build Docker Image') {
            echo "🐳 Сборка Docker-образа: ${imageName}:${imageTag}"
            
            // Создаём простой Dockerfile если нет своего
            if (!fileExists('Dockerfile')) {
                writeFile file: 'Dockerfile', text: """
FROM nginx:alpine
COPY . /usr/share/nginx/html
EXPOSE ${port}
CMD ["nginx", "-g", "daemon off;"]
"""
            }
            
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
            
            echo "✅ Контейнер запущен"
        }
        
        stage('Health Check') {
            echo "🏥 Проверка здоровья приложения..."
            
            retry(5) {
                sleep 3
                
                // Проверка состояния контейнера
                def containerStatus = sh(
                    script: "docker inspect -f '{{.State.Status}}' ${containerName} 2>/dev/null || echo 'not-found'",
                    returnStdout: true
                ).trim()
                
                if (containerStatus != 'running') {
                    error "❌ Контейнер не запущен (статус: ${containerStatus})"
                }
                
                echo "✅ Контейнер работает (статус: ${containerStatus})"
                
                // HTTP-проверка (если приложение веб)
                try {
                    def httpCode = sh(
                        script: "curl -s -o /dev/null -w '%{http_code}' ${appUrl} --max-time 5 || echo '000'",
                        returnStdout: true
                    ).trim()
                    
                    if (httpCode.startsWith('2') || httpCode.startsWith('3')) {
                        echo "✅ HTTP-статус: ${httpCode}"
                    } else {
                        echo "⚠ HTTP-статус: ${httpCode}"
                        // Не падаем сразу, даём ещё попытки
                        if (httpCode == '000') {
                            error "Сервис не отвечает"
                        }
                    }
                } catch (Exception e) {
                    echo "⚠ Ошибка HTTP-проверки: ${e.message}"
                }
            }
        }
    }
    
    echo "🎉 Деплой завершён успешно!"
}

return this