
pipeline {
    agent any

    stages {

        stage('Download Code') {
            steps {
                echo 'Student Attendance code downloaded successfully'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '"C:\\Users\\Ashok\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" --version'

                bat '"C:\\Users\\Ashok\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -m pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                bat '"C:\\Users\\Ashok\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -m py_compile app.py'
                echo 'Student Attendance application test completed!'
            }
        }

        stage('Build Completed') {
            steps {
                echo 'Student Attendance Pipeline Successful!'
            }
        }
    }
}
