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
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    playwright install --with-deps ${BROWSER}
                '''
            }
        }

        stage('🧪 Execute Tests') {
            steps {
                script {
                    def markerFlag = params.MARKERS ? "-m \"${params.MARKERS}\"" : ""
                    def headedFlag = params.HEADED ? "--headed" : ""
                    sh """
                        . .venv/bin/activate
                        pytest tests/ \
                            --browser-name=${params.BROWSER} \
                            --base-url=${params.BASE_URL} \
                            ${headedFlag} \
                            ${markerFlag} \
                            --alluredir=${ALLURE_RESULTS} \
                            --tb=short \
                            -v \
                            || true
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
