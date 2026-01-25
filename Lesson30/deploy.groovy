#!/usr/bin/env groovy

// Функция для запуска из Jenkinsfile
def runDeploy() {
    def imageName = 'app'
    def imageTag = 'latest'
    def containerName = 'app-dev'
    def port = 8080
    
    node {
        stage('Build') {
            echo "Сборка образа: ${imageName}:${imageTag}"
            
            sh """
                cat > Dockerfile << EOF
FROM nginx:alpine
RUN echo 'Hello from Jenkins' > /usr/share/nginx/html/index.html
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
    }
}

// Автоматический запуск при загрузке
runDeploy()