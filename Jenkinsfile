pipeline {
    agent any

    environment {
        PROJECT_DIR = '/opt/Cupuacu'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Run docker-compose tests') {
            when {
                not {
                    branch 'main' // Só roda testes se NÃO for main
                }
            }
            steps {
                sh '''
                docker compose -f docker-compose.test.yml up --abort-on-container-exit --build
                '''
            }
        }

        stage('Tear down containers') {
            when {
                not {
                    branch 'main'
                }
            }
            steps {
                sh '''
                docker compose -f docker-compose.test.yml down
                '''
            }
        }

        stage('Clean up Docker') {
            when {
                not {
                    branch 'main'
                }
            }
            steps {
                sh 'docker image prune -f'
            }
        }

        stage('Deploy on Merge to Main') {
            when {
                branch 'main' // Só executa se for na main
            }
            steps {
                dir("${env.PROJECT_DIR}") {
                    sh '''
                    echo "Atualizando repositório..."
                    git pull origin main

                    echo "Derrubando containers existentes..."
                    docker compose down

                    echo "Subindo nova versão em segundo plano..."
                    docker compose up -d
                    '''
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline finalizado'
        }
    }
}
