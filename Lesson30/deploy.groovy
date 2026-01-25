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
            
            // Создаём Dockerfile с простым веб-сервером
            writeFile file: 'Dockerfile', text: """
FROM nginx:alpine
RUN echo "<!DOCTYPE html>
<html>
<head><title>ТМС Приложение</title>
<style>
body {{ font-family: Arial; margin: 40px; }}
.header {{ background: #4CAF50; color: white; padding: 20px; }}
.content {{ padding: 20px; }}
</style>
</head>
<body>
<div class='header'>
<h1>🚀 ТМС Приложение развёрнуто!</h1>
<p>Pipeline успешно выполнен</p>
</div>
<div class='content'>
<h2>Информация о деплое:</h2>
<ul>
<li>Окружение: ${config.environment ?: 'dev'}</li>
<li>Версия: ${config.imageTag ?: 'latest'}</li>
<li>Сборка: ${config.buildNumber ?: 'N/A'}</li>
<li>Время: \$(date)</li>
</ul>
<p>Статус: <span style='color: green; font-weight: bold;'>✅ Работает</span></p>
</div>
</body>
</html>" > /usr/share/nginx/html/index.html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
"""
            
            sh "docker build -t ${imageName}:${imageTag} ."
        }
        
        stage('Deploy Container') {
            echo "🚀 Развёртывание контейнера: ${containerName}"
            
            // Останавливаем и удаляем старый контейнер
            sh """
                docker stop ${containerName} 2>/dev/null || true
                docker rm ${containerName} 2>/dev/null || true
            """
            
            // Запускаем новый контейнер с веб-сервером
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
                def containerStatus = sh(
                    script: "docker inspect -f '{{.State.Status}}' ${containerName} 2>/dev/null || echo 'not-found'",
                    returnStdout: true
                ).trim()
                
                if (containerStatus != 'running') {
                    error "❌ Контейнер не запущен (статус: ${containerStatus})"
                }
                
                echo "✅ Контейнер работает (статус: ${containerStatus})"
                
                // HTTP-проверка
                def httpCode = sh(
                    script: "curl -s -o /dev/null -w '%{http_code}' ${appUrl} --max-time 10 || echo '000'",
                    returnStdout: true
                ).trim()
                
                if (httpCode == '200') {
                    echo "✅ HTTP-статус: ${httpCode} - Приложение доступно"
                } else {
                    echo "⚠ HTTP-статус: ${httpCode} - Проблемы с доступностью"
                    // Проверяем логи контейнера
                    sh """
                        echo "Логи контейнера:"
                        docker logs ${containerName} --tail 10 2>/dev/null || echo "Логи недоступны"
                    """
                    if (httpCode == '000') {
                        error "Сервис не отвечает на HTTP запросы"
                    }
                }
            }
            
            // Дополнительная проверка - получаем заголовок страницы
            sh """
                echo "Проверка содержимого страницы..."
                curl -s ${appUrl} | grep -q "ТМС Приложение" && echo "✅ Контент страницы корректный" || echo "⚠ Проблемы с контентом"
            """
        }
    }
    
    echo "🎉 Деплой завершён успешно!"
}

return this