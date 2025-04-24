pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'your-django-app:latest'
        COMPOSE_FILE = 'docker-compose.yml'
    }

    stages {
        stage('Clone Repo') {
            steps {
                git 'https://github.com/your-username/your-django-repo.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker-compose build'
                }
            }
        }

        stage('Run Migrations & Collect Static') {
            steps {
                script {
                    sh 'docker-compose run web python manage.py migrate'
                    sh 'docker-compose run web python manage.py collectstatic --noinput'
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    sh 'docker-compose up -d'
                }
            }
        }
    }
}
