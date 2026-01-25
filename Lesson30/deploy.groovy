#!/usr/bin/env groovy

// Функция для запуска из Jenkinsfile
def runDeploy() {
    def imageName = 'app'
    def imageTag = 'latest'
    def containerName = 'app-dev'
    def port = 9090  // Изменили порт с 8080 на 9090
    
    node {
        stage('Build') {
            echo "Сборка образа: ${imageName}:${imageTag}"
            
            sh """
                cat > Dockerfile << EOF
FROM nginx:alpine
RUN echo 'Hello from Jenkins Pipeline' > /usr/share/nginx/html/index.html
EOF
                docker build -t ${imageName}:${imageTag} .
            """
        }
        
        stage('Deploy') {
            echo "Запуск контейнера: ${containerName}"
            
            sh """
                docker stop ${containerName} 2>/dev/null || true
                docker rm ${containerName} 2>/dev/null || true
                docker run -d --name ${containerName} -p ${port}:80 ${imageName}:${imageTag}
                echo "Контейнер запущен на порту ${port}"
            """
        }
        
        stage('Check') {
            echo "Проверка"
            
            retry(3) {
                sleep 2
                sh """
                    docker inspect -f '{{.State.Status}}' ${containerName} | grep -q running
                    echo "✅ Контейнер работает"
                    
                    # Проверка HTTP
                    if curl -s http://localhost:${port} > /dev/null; then
                        echo "✅ Приложение доступно"
                    else
                        echo "⚠ Проблемы с подключением"
                    fi
                """
            }
        }
    }
}

// Автоматический запуск при загрузке
runDeploy()