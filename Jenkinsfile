pipeline {
    agent any

    environment {
        CONTAINER_ID = ""
        SUM_PY_PATH = "/app/sum.py"
        DIR_PATH = "."
        TEST_FILE_PATH = "test_variables.txt"
        IMAGE_NAME = "sum-python-image"
        DOCKERHUB_USER = credentials('dockerhub-username')
        DOCKERHUB_PASS = credentials('dockerhub-password')
        IMAGE_TAG = "latest"
        DOCKERHUB_CREDENTIALS= credentials('6d7d1e78-2884-4ac3-9ad7-522efa02381f')
    }
    stages {

        stage('Build') {
            steps {
                sh "docker build -t ${IMAGE_NAME} ${DIR_PATH}"
            }
        }
    }
    stage('Run') {
    steps {
        script {
            def output = sh(
                script: "docker run -d ${IMAGE_NAME}",
                returnStdout: true
            )
            def lines = output.split('\n')
            CONTAINER_ID = lines[-1].trim()

        }
    }
}

    stage('Test') {
        steps {
            script {
                def testLines = readFile(TEST_FILE_PATH).split('\n')

                for (line in testLines) {

                    if (line.trim() == "") {
                        continue
                    }

                    def vars = line.split(' ')
                    def arg1 = vars[0]
                    def arg2 = vars[1]
                    def expectedSum = vars[2].toFloat()
                    def output = sh(script: "docker exec ${CONTAINER_ID} python /app/sum.py ${arg1} ${arg2}", returnStdout: true).trim()
                    def result = output.toFloat()

                    if (result == expectedSum) {
                        echo "Bravo, le test est une réussite : ${arg1} + ${arg2} = ${result}"
                    } else {
                        error "Erreur, le test a échoué : ${arg1} + ${arg2} = ${result},ce que nous voulions obtenir : ${expectedSum} veuillez recommencer !"
                    }
                }
            }
        }
    }
    stage('Deploy') {
        steps {
            script {
            withCredentials([usernamePassword(credentialsId: '6d7d1e78-2884-4ac3-9ad7-522efa02381f', passwordVariable: 'DOCKERHUB_CREDENTIALS_PSW', usernameVariable: 'DOCKERHUB_CREDENTIALS_USR')]) {
            sh """ echo "Début de la Connexion à DockerHub..." echo "${DOCKERHUB_PASS}" | docker login -u ${DOCKERHUB_CREDENTIALS_USR} -p ${DOCKERHUB_CREDENTIALS_PSW}
             echo "Connexion à DockerHub réussi..."
            echo "Tag de l'image en cours..." docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:${IMAGE_TAG}
            echo "Tag de l'image réussi"
                    echo "Push de l'image en cours..."
                    docker push ${IMAGE_NAME}:${IMAGE_TAG}
                    echo "Push de l'image réussi..."
            """
            }}
            }
        }
    post {
        always {
            script {
                if (CONTAINER_ID?.trim()) {
                    echo "Test terminé, on arrête le docker ${CONTAINER_ID}"
                    sh "docker stop ${CONTAINER_ID}"

                    echo "Le docker est arrêté, maintenant on le supprime ${CONTAINER_ID}"
                    sh "docker rm ${CONTAINER_ID}"
                } else {
                    echo "Aucun conteneur n'a besoin d'être arrêté pour le moment."
                }
                sh "docker logout"
            }
        }
    }

}