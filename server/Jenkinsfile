pipeline {
    agent any 
    stages {
        stage("Test") {
            steps {
                echo "Test test test."
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