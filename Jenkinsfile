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
                expression { env.CHANGE_ID != null }
            }
            steps {
                sh '''
                docker compose -f docker-compose.test.yml up --abort-on-container-exit --build
                '''
            }
        }

        stage('Tear down containers') {
            when {
                expression { env.CHANGE_ID != null }
            }
            steps {
                sh '''
                docker compose -f docker-compose.test.yml down
                '''
            }
        }

        stage('Clean up Docker') {
            when {
                expression { env.CHANGE_ID != null }
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
