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
                    env.IMAGE_NAME = "neverquest-server"
                    env.IMAGE_TAG = "latest"
                    env.REGION = "us-west-2"
                    sh "docker tag ${env.IMAGE_NAME}:${env.IMAGE_TAG} ${env.ACCOUNT_ID}.dkr.ecr.${env.REGION}.amazonaws.com/${env.IMAGE_NAME}:${env.IMAGE_TAG}"
                }
            }
        }
        stage("Push image to ECR") {
            steps {
                script {
                    sh "aws ecr get-login-password --region ${env.REGION} | docker login --username AWS --password-stdin ${env.ACCOUNT_ID}.dkr.ecr.${env.REGION}.amazonaws.com"
                }
                script {
                    sh "docker push ${env.ACCOUNT_ID}.dkr.ecr.${env.REGION}.amazonaws.com/${env.IMAGE_NAME}:${env.IMAGE_TAG}"
                }
            }
        }
        stage("Remove image") {
            steps {
                script {
                    sh "docker rmi ${env.IMAGE_NAME}:${env.IMAGE_TAG} ${env.ACCOUNT_ID}.dkr.ecr.${env.REGION}.amazonaws.com/${env.IMAGE_NAME}:${env.IMAGE_TAG}"
                }
            }
        }
    }
}