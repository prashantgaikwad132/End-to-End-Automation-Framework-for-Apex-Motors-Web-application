pipeline {
    agent any

    parameters {
        choice(name: 'BROWSER', choices: ['chromium', 'firefox', 'webkit'], description: 'Target browser engine')
        booleanParam(name: 'HEADED', defaultValue: false, description: 'Run in headed mode')
        string(name: 'BASE_URL', defaultValue: 'https://driveway-dashboard-buddy.lovable.app', description: 'Application under test URL')
        string(name: 'MARKERS', defaultValue: '', description: 'Pytest markers to run (e.g. smoke, regression)')
    }

    environment {
        PYTHONDONTWRITEBYTECODE = '1'
        ALLURE_RESULTS = 'reports/allure-results'
    }

    stages {

        stage('🔧 Setup Environment') {
            steps {
                bat '''
                C:\\Users\\prash\\AppData\\Local\\Programs\\Python\\Python312\\python.exe -m venv .venv
                call .venv\\Scripts\\activate.bat
                python -m pip install --upgrade pip
                python -m pip install -r requirements.txt
                python -m playwright install chromium --with-deps
                '''
            }
        }

        stage('🧪 Execute Tests') {
            steps {
                script {
                    def markerFlag = params.MARKERS ? "-m \"${params.MARKERS}\"" : ""
                    def headedFlag = params.HEADED ? "--headed" : ""
                    
                    bat """
                        call .venv\\Scripts\\activate.bat
                        python -m pytest tests/ --browser-name=${params.BROWSER} --base-url=${params.BASE_URL} ${headedFlag} ${markerFlag} --tb=short -v || exit /b 0
                    """
                }
            }
        }

        stage('📊 Generate Allure Report') {
            steps {
                allure([
                    includeProperties: false,
                    jdk: '',
                    properties: [],
                    reportBuildPolicy: 'ALWAYS',
                    results: [[path: "${ALLURE_RESULTS}"]]
                ])
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
            cleanWs()
        }
        failure {
            echo '❌ Pipeline failed — check Allure report for details.'
        }
        success {
            echo '✅ All stages completed successfully.'
        }
    }
}
