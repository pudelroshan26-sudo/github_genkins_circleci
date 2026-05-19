pipeline {
    agent any

    stages {
        stage('Initialize') {
            steps {
                echo 'Starting comparative pipeline benchmarks...'
            }
        }

        stage('Benchmark Project A (Node.js API)') {
            steps {
                dir('project_a_node_api') {
                    echo 'Running Project A tests...'
                    sh 'npm install'
                    sh 'npm test'
                }
            }
        }

        stage('Benchmark Project B (Python Flask App)') {
            steps {
                dir('project_b_python_flask') {
                    echo 'Running Project B tests...'
                    sh 'python -m pip install --upgrade pip'
                    sh 'pip install -r requirements.txt'
                    sh 'pytest'
                }
            }
        }

        stage('Benchmark Project C (Docker Microservices)') {
            parallel {
                stage('Build Auth Service') {
                    steps {
                        dir('project_c_microservices/service_auth') {
                            echo 'Building Auth Service Docker Image...'
                            sh 'docker build -t service_auth:latest .'
                        }
                    }
                }
                stage('Build API Service') {
                    steps {
                        dir('project_c_microservices/service_api') {
                            echo 'Building API Service Docker Image...'
                            sh 'docker build -t service_api:latest .'
                        }
                    }
                }
                stage('Build Web Service') {
                    steps {
                        dir('project_c_microservices/service_web') {
                            echo 'Building Web Service Docker Image...'
                            sh 'docker build -t service_web:latest .'
                        }
                    }
                }
            }
        }
    }

    post {
        always {
            echo 'Benchmark runs finished.'
        }
    }
}
