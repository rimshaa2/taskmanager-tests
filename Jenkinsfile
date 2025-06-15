pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/rimshaa2/taskmanager-tests.git'
            }
        }
        stage('Build Test Image') {
            steps {
                script {
                    docker.build("taskmanager-tests:latest", "--file Dockerfile .")
                }
            }
        }
        stage('Run Tests') {
            steps {
                script {
                    docker.image("taskmanager-tests:latest").inside {
                        sh 'pytest tests/'  # Or `mvn test` for Java
                    }
                }
            }
        }
    }
    post {
        always {
            emailext (
                subject: "Test Results: ${currentBuild.result ?: 'SUCCESS'}",
                body: "Test results: ${env.BUILD_URL}",
                to: "collaborator@example.com"  # Replace with your email
            )
        }
    }
}
