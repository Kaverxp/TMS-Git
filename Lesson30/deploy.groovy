#!/usr/bin/env groovy

def call(Map config = [:]) {
    def imageName = config.imageName ?: 'app'
    def imageTag = config.imageTag ?: 'latest'
    def containerName = config.containerName ?: 'app-container'
    def port = config.port ?: 8080
    
    node {
        stage('Build') {
            echo "Сборка образа: ${imageName}:${imageTag}"
            
            sh """
                cat > Dockerfile << EOF
FROM nginx:alpine
RUN echo 'Hello from Docker' > /usr/share/nginx/html/index.html
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
            """
        }
        
        stage('Check') {
            echo "Проверка"
            
            retry(3) {
                sleep 2
                sh """
                    docker inspect -f '{{.State.Status}}' ${containerName} | grep -q running
                    echo "Контейнер запущен"
                """
            }
        }
    }
}

// Удаляем return this - это вызывает проблему