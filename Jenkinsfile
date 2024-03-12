pipeline {
    agent any 
    stages {
        stage("Test") {
            steps {
                def user = sh(script: 'whoami', returnStdout: true).trim()
                echo "${user} is running this job"
            }
        }
        stage("Build image") {
            steps {
                dir('server') {
                    sh "./build.sh"
                }
            }
        }
    }
}