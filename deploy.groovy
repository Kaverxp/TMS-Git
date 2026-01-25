#!/usr/bin/env groovy

def call(Map config = [:]) {
    node {
        stage('Deploy Application') {
            echo "Deploying with config: ${config}"
            
            // Ваши шаги деплоя
            sh "docker build -t ${config.imageName ?: 'app'}:${config.imageTag ?: 'latest'} ."
            sh """
                docker stop ${config.containerName ?: 'app-container'} 2>/dev/null || true
                docker rm ${config.containerName ?: 'app-container'} 2>/dev/null || true
            """
            sh """
                docker run -d \
                    --name ${config.containerName ?: 'app-container'} \
                    -p ${config.port ?: 8080}:${config.port ?: 8080} \
                    ${config.imageName ?: 'app'}:${config.imageTag ?: 'latest'}
            """
        }
    }
}

return this