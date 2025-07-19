pipeline {
    agent { label 'docker' }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Run docker-compose tests') {
            steps {
                sh '''
                docker compose -f docker-compose.test.yml up --abort-on-container-exit --build
                '''
            }
        }

        stage('Tear down containers') {
            steps {
                sh '''
                docker compose -f docker-compose.test.yml down
                '''
            }
        }

        stage('Clean up Docker') {
            steps {
                sh 'docker image prune -f'
            }
        }
    }

    post {
        always {
            echo 'Pipeline finalizado'
        }
    }
}
