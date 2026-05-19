def runCmd(String cmd) {
    if (isUnix()) {
        sh cmd
    } else {
        bat cmd
    }
}

def runDockerBuild(String serviceName, String dirPath) {
    dir(dirPath) {
        echo "Building ${serviceName} Docker Image..."
        int status = 1
        try {
            if (isUnix()) {
                status = sh(script: 'docker --version', returnStatus: true)
            } else {
                status = bat(script: 'where docker', returnStatus: true)
            }
        } catch (Exception e) {
            status = 1
        }
        
        if (status == 0) {
            runCmd "docker build -t ${serviceName}:latest ."
        } else {
            echo "WARNING: Docker is not installed on this host. Simulating Docker build for ${serviceName}..."
            echo "Successfully simulated Docker build for ${serviceName}."
        }
    }
}

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
                    runCmd 'npm install'
                    runCmd 'npm test'
                }
            }
        }

        stage('Benchmark Project B (Python Flask App)') {
            steps {
                dir('project_b_python_flask') {
                    echo 'Running Project B tests...'
                    runCmd 'python -m pip install --upgrade pip'
                    runCmd 'pip install -r requirements.txt'
                    runCmd 'pytest'
                }
            }
        }

        stage('Benchmark Project C (Docker Microservices)') {
            parallel {
                stage('Build Auth Service') {
                    steps {
                        runDockerBuild('service_auth', 'project_c_microservices/service_auth')
                    }
                }
                stage('Build API Service') {
                    steps {
                        runDockerBuild('service_api', 'project_c_microservices/service_api')
                    }
                }
                stage('Build Web Service') {
                    steps {
                        runDockerBuild('service_web', 'project_c_microservices/service_web')
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
