pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/rimshaa2/taskmanager-tests.git'
            }
        }
        stage('Run Tests') {
            steps {
                script {
                    docker.build("taskmanager-tests:latest", "--file Dockerfile .")
                    docker.image("taskmanager-tests:latest").inside {
                        sh 'pytest tests/'
                    }
                }
            }
        }
    }
    post {
        always {
            emailext (
                subject: "Test Results: ${currentBuild.result ?: 'SUCCESS'}",
                body: "View results: ${env.BUILD_URL}",
                to: "rimshasajid2004@example.com"
            )
        }
    }
}
