pipeline {
    agent any
    
    stages {
        stage('Requirements Package Installation') {
            steps {
                sh 'sudo pip install -r /home/ana-moeez-2/lab4/requirements.txt'
            }
        }
        stage('Run Unit Testing') {
            steps {
                sh 'sudo python3.10  /home/ana-moeez-2/lab4/unit_testing.py'
            }
        }
    }
}