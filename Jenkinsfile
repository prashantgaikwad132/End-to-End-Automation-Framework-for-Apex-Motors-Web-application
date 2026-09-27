pipeline {
    agent any

    parameters {
        choice(name: 'BROWSER', choices: ['chromium', 'firefox', 'webkit'], description: 'Target browser engine')
        string(name: 'BASE_URL', defaultValue: 'https://driveway-dashboard-buddy.lovable.app', description: 'Application under test URL')
        string(name: 'MARKERS', defaultValue: '', description: 'Pytest markers to run (e.g. smoke, regression)')
    }

    environment {
        PYTHONDONTWRITEBYTECODE = '1'
        ALLURE_RESULTS = 'reports/allure-results'
    }

    stages {
        stage('🧪 Execute Playwright Tests in Docker') {
            agent {
                docker {
                    image 'mcr.microsoft.com/playwright/python:v1.49.1-noble'
                    args '--ipc=host -u root:root'
                    reuseNode true
                }
            }
            steps {
                script {
                    def markerFlag = params.MARKERS ? "-m \"${params.MARKERS}\"" : ""

                    sh """
                        python3 -m pip install --upgrade pip
                        pip install -r requirements.txt
                        pytest tests/ -n 4 \
                            --browser=${params.BROWSER} \
                            --base-url=${params.BASE_URL} \
                            ${markerFlag} \
                            --alluredir=reports/allure-results \
                            --tracing=retain-on-failure \
                            --tb=short -v || true
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
                    results: [[path: 'reports/allure-results']]
                ])
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'test-results/**/*.zip, reports/**', allowEmptyArchive: true
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