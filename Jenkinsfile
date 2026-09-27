pipeline {
    agent any

    parameters {
        choice(name: 'BROWSER', choices: ['chromium', 'firefox', 'webkit'], description: 'Target browser engine')
        choice(name: 'MARKERS', choices: ['', 'smoke', 'regression', 'inventory', 'contact', 'navigation', 'responsive'], description: 'Pytest markers to execute')
        choice(name: 'WORKERS', choices: ['2', '1', '4'], description: 'Parallel execution workers')
    }

    environment {
        ALLURE_RESULTS = 'reports/allure-results'
        IMAGE_NAME     = 'mcr.microsoft.com/playwright/python:v1.49.1-noble'
    }

    stages {
        stage('🧪 Execute Playwright Tests in Docker') {
            steps {
                script {
                    def markerFlag = params.MARKERS ? "-m ${params.MARKERS}" : ""

                    bat """
                        docker run --rm ^
                            -v "%WORKSPACE%":/workspace ^
                            -w /workspace ^
                            ${IMAGE_NAME} ^
                            /bin/bash -c "pip install --no-cache-dir -r requirements.txt pytest-xdist && pytest tests/ --browser ${params.BROWSER} -n ${params.WORKERS} ${markerFlag} --alluredir=${ALLURE_RESULTS} --clean-alluredir -v || true"
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
        }
        failure {
            echo '❌ Pipeline execution failed — review logs or Allure report.'
        }
        success {
            echo '✅ Pipeline execution completed successfully.'
        }
    }
}