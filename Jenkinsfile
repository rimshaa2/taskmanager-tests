pipeline {
    agent any
    
    environment {
        // Removed DOCKER_BUILDKIT as it's causing issues
        TEST_IMAGE = "taskmanager-tests"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout([$class: 'GitSCM', 
                         branches: [[name: '*/main']],
                         userRemoteConfigs: [[url: 'https://github.com/rimshaa2/taskmanager-tests.git']]
                        ])
            }
        }
        
        stage('Build Test Image') {
            steps {
                script {
                    try {
                        // Simple docker build without BuildKit
                        sh 'docker build -t ${TEST_IMAGE}:latest .'
                    } catch (Exception e) {
                        error("Docker build failed: ${e.getMessage()}")
                    }
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                script {
                    try {
                        // Run tests with proper directory structure
                        docker.image("${TEST_IMAGE}:latest").inside {
                            sh 'pytest tests/ --verbose --html=report.html'
                        }
                        
                        // Archive test results (optional)
                        junit '**/test-reports/*.xml'
                        archiveArtifacts '**/report.html'
                    } catch (Exception e) {
                        error("Tests failed: ${e.getMessage()}")
                    }
                }
            }
        }
    }
    
    post {
        always {
            echo "Build completed with status: ${currentBuild.result}"
            // Optional: Add clean up step
            sh 'docker rmi -f ${TEST_IMAGE}:latest || true'
        }
    }
}
