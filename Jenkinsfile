pipeline {
    agent any
    environment {
        CONTAINER_ID = ''
        SUM_PY_PATH = 'C:/Users/ThinkPad/Desktop/school/tp devops jenkins/sum.py'
        DIR_PATH = 'C:/Users/ThinkPad/Desktop/school/tp devops jenkins'
        TEST_FILE_PATH = 'C:/Users/ThinkPad/Desktop/school/tp devops jenkins/test_variables.txt'
        DOCKERHUB_CREDENTIALS= credentials('6d7d1e78-2884-4ac3-9ad7-522efa02381f')
    }
    stages {
        stage('Build') {
            steps {
                bat ("docker build -t sumpy .")
            }
        }
        stage('Run'){
            def output = bat ( script : 'docker run -it -d pysum' , return Stdout:true )
            def lines = output.split('\n')
            CONTAINER_ID = lines[-1].trim()
        }
        stage('Test'){
            def testLines = readFile(TEST_FILE_PATH).split('\n')
            for(lineintestLines) {
                def vars = line.split(' ')
                def arg1 = vars[0]
                def arg2 = vars[1]
                def expectedSum = vars[2].toFloat()
                def output = bat (script:"docker exec ${CONTAINER_ID} python sum.py " + arg1 + " " + arg2,return Stdout:true)
                def result = output.split('\n')[-1].trim().toFloat()
                if (result == expectedSum){
                    echo "TEST PASSED"
                } else {
                    error "TEST FAILED"
                }

            }
        }
        stage('post') {
            bat ("docker rm --force ${CONTAINER_ID}")
        }
        stage('Deploy'){
            withCredentials([usernamePassword(credentialsId: '6d7d1e78-2884-4ac3-9ad7-522efa02381f', passwordVariable: 'DOCKERHUB_CREDENTIALS_PSW', usernameVariable: 'DOCKERHUB_CREDENTIALS_USR')]) {
            bat ("docker login -u ${DOCKERHUB_CREDENTIALS_USR} -p ${DOCKERHUB_CREDENTIALS_PSW}")
        }
    }
}