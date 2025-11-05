pipeline {
    agent any

    environment{
        VENV_PATH = "${WORKSPACE}\\.venv"
        ACTIVATE = "call ${WORKSPACE}\\.venv\\Scripts\\activate"
    }
    stages{
        stage('Checkout Code') {
            steps {
               git branch: 'main',
               credentialsId: 'github_token',
               url: 'https://github.com/Biophilia18/api_auto.git'
            }
        }
        stage('Setup Virtual Env') {
            steps {
                bat """
                if not exist %VENV_PATH% (python -m venv %VENV_PATH%)
                %ACTIVATE%
                pip install --upgrade pip
                pip install -r requirements.txt
                """
            }
        }
        stage('Run Tests') {
            steps{
                bat """
                %ACTIVATE%
                pytest --allure=reports/allure_raw
                """
            }
        }
        stage('Create Allure Report'){
            steps{
                bat"""
                %ACTIVATE%
                allure generate reports/allure_raw -o reports/allure_report --clean
                """
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'reports/allure_report/**', fingerprint: true
        }
    }
}
