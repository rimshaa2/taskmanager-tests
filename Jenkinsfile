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
                        error("Docker build failed: ${e.toString()}")
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
                        error("Tests failed: ${e.toString()}")
                    }
                }
            }
        }
    }
    
    post {
        always {
            // Removed email notification
            echo "Build completed with status: ${currentBuild.result}"
        }
    }
}
