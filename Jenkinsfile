pipeline {
    agent any

    environment {
        DJANGO_SETTINGS_MODULE = 'bookstore.settings'
    }

    stages {
        stage('Clone Repository') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker-compose build'
            }
        }

        stage('Apply Migrations') {
            steps {
                sh 'docker-compose run web python manage.py migrate'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'docker-compose run web python manage.py test'
            }
        }

        stage('Collect Static Files') {
            steps {
                sh 'docker-compose run web python manage.py collectstatic --noinput'
            }
        }

        stage('Start Application') {
            steps {
                sh 'docker-compose up -d'
            }
        }
    }

    post {
        failure {
            echo '❌ Build Failed'
        }
        success {
            echo '✅ Bookstore App Deployed Successfully'
        }
    }
}
