pipeline{
    agent any

    triggers{
        pollSCM('H/5 * * * *')
    }

    parameters{
        string(name:'BRANCH_NAME', defaultValue: 'main', description: ' Git branch to build')
        choice(name: 'DEPLOY_ENV', choices: ['dev', 'uat', 'prod'], description: 'Deployment env')

    }

    environment{
        APP_NAME = "payment-service"
        DOCKER_REPO = "nikhilgowda/payment-service"
    }

    stages{

        stage("Checkout code"){
            steps{
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: "*/${params.BRANCH_NAME}]],
                    userRemoteConfigs: [[
                        url: "https://github.com/"
                    ]]
                ])
            }
        }

        stage("Build application"){
            steps{
                retry(3){
                    sh 'mvn clean package'
                }
            }
        }

        stage('Tests and scan'){
            parallel{
                stage('Unit Test'){
                    steps{
                        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE'){
                            sh 'mvn test'
                        }
                    }
                }

                stage('SonarQube scan'){
                    steps{
                        sh 'mvn sonar:sonar'
                    }
                }

                stage('Build Docker image'){
                    when{
                        anyOf{
                            environment name: 'DEPLOY_ENV', value: 'prod'
                            environment name: 'DEPLOY_ENV', value: 'uat'

                        }
                        steps{
                            sh """
                                docker build -t ${DOCKER_REPO}:${BUILD_NUMBER}
                            """
                        }
                    }
                }

                post{
                    always{
                            echo "Execution completed"
                    }

                    success{
                            echo "Pipeline Successful"

                    }

                    unstable{
                            echo "Pipeline is unstable"

                    }

                    failure{
                        echo "Pipeline failed"
                    }
                }
            }
        }
    }
}