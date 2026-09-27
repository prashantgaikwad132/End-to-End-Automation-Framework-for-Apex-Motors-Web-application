pipeline {
    agent {
        docker {
            // Pre-configured official image containing Python and browser binaries
            image 'mcr.microsoft.com/playwright/python:v1.49.1-noble'
            // --ipc=host provides shared memory so headless browsers do not crash
            args '--ipc=host -u root:root'
        }
    }

    parameters {
        choice(name: 'BROWSER', choices: ['chromium', 'firefox', 'webkit'], description: 'Target browser engine')
        string(name: 'BASE_URL', defaultValue: 'https://driveway-dashboard-buddy.lovable.app', description: 'Application under test URL')
        string(name: 'MARKERS', defaultValue: '', description: 'Pytest markers to run (e.g. smoke, regression)')
    }

    environment {
        PYTHONDONTWRITEBYTECODE = '1'
        ALLURE_RESULTS = 'reports/allure-results'
        HOME = '/tmp'
    }

    stages {
        stage('🔧 Install Dependencies') {
            steps {
                // Runs inside the Linux Docker container
                sh '''
                    python3 -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('🧪 Execute Tests') {
            steps {
                script {
                    def markerFlag = params.MARKERS ? "-m \"${params.MARKERS}\"" : ""
                    
                    // Runs Pytest inside the container; || true ensures report generation runs even on test failures
                    sh """
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