pipeline {
    agent any 
    stages {
        stage("Test") {
            steps {
                echo "$(whoami) is running this job"
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