pipeline {
    agent any 
    stages {
        stage("Test") {
            steps {
                script {
                    def user = sh(script: 'whoami', returnStdout: true).trim()
                    echo "${user} is running this job"
                }
            }
        }
        stage("Build image") {
            steps {
                dir('server') {
                    sh "./build.sh"
                }
            }
        }
        stage("Re-tag image") {
            steps {
                script {
                    def ACCOUNT_ID = sh(returnStdout: true, script: 'aws sts get-caller-identity --query "Account" --output text').trim()
                    env.ACCOUNT_ID = ACCOUNT_ID
                    sh "docker tag neverquest-server:latest ${env.ACCOUNT_ID}.dkr.ecr.us-west-2.amazonaws.com/neverquest-server:latest"
                }
            }
        }
        stage("Push image to ECR") {
            steps {
                script {
                    sh "docker push ${env.ACCOUNT_ID}.dkr.ecr.us-west-2.amazonaws.com/neverquest-server:latest"
                }
            }
        }
    }
}