pipeline {
    agent any
    
    environment {
        DOCKER_BUILDKIT = "1"  
    }
    
    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/rimshaa2/taskmanager-tests.git'
            }
        }
        
        stage('Build Test Image') {
            steps {
                script {
                    try {
                        sh 'docker build --no-cache -t taskmanager-tests:latest .'
                    } catch (Exception e) {
                        emailext (
                            subject: "FAILED: Docker Build - ${env.JOB_NAME}",
                            body: "Build failed: ${e.toString()}\n\nCheck console: ${env.BUILD_URL}",
                            to: 'rimshasajid2004@gmail.com'
                        )
                        error("Docker build failed")
                    }
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                script {
                    try {
                        docker.image('taskmanager-tests:latest').inside {
                            sh 'pytest tests/ --verbose'
                        }
                    } catch (Exception e) {
                        emailext (
                            subject: "FAILED: Tests - ${env.JOB_NAME}",
                            body: "Tests failed: ${e.toString()}\n\nCheck console: ${env.BUILD_URL}",
                            to: 'rimshasajid2004@gmail.com'
                        )
                        error("Tests failed")
                    }
                }
            }
        }
    }
    
    post {
        always {
            emailext (
                subject: "Result: ${currentBuild.result} - ${env.JOB_NAME}",
                body: "Build: ${env.BUILD_URL}\n\nStatus: ${currentBuild.result}",
                to: 'rimshasajid2004@gmail.com',
                attachLog: true
            )
        }
    }
}
