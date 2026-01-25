// Jenkinsfile для репозитория TMS-Git
pipeline {
    agent any
    
    triggers {
        pollSCM('H/5 * * * *') // Проверка изменений каждые 5 минут
    }
    
    options {
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }
    
    parameters {
        choice(name: 'ENV', choices: ['dev', 'prod'], description: 'Environment')
        string(name: 'VERSION', defaultValue: '1.0.0', description: 'App version')
    }
    
    stages {
        stage('Checkout and Analyze') {
            steps {
                checkout scm
                sh '''
                    echo "Repository structure:"
                    tree -L 2 || find . -type f -name "*.java" -o -name "*.groovy" -o -name "*.xml" -o -name "*.gradle" | head -30
                '''
            }
        }
        
        stage('Test Groovy Script Integration') {
            steps {
                script {
                    // Пробуем загрузить deploy.groovy
                    if (fileExists('deploy.groovy')) {
                        echo "Found deploy.groovy, loading..."
                        def deploy = load 'deploy.groovy'
                        
                        // Простой тест
                        deploy.call([
                            testMode: true,
                            message: "Test from TMS-Git pipeline"
                        ])
                    } else {
                        echo "No deploy.groovy found, creating test script..."
                        
                        // Создаём тестовый скрипт
                        writeFile file: 'test-deploy.groovy', text: '''
def call(params) {
    echo "Test Groovy Script from TMS-Git"
    echo "Params: ${params}"
    
    node {
        stage('Test') {
            sh 'echo "Hello from inline Groovy script"'
            sh 'docker --version'
        }
    }
}
'''
                        
                        def testScript = load 'test-deploy.groovy'
                        testScript.call([test: true])
                    }
                }
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
    }
}