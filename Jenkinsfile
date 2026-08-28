pipeline {
    agent any
    environment {
        IMAGE = "eberepion/velos-api"
        TAG = "${env.BUILD_NUMBER}"
    }
    stages {
        stage('Tester') {
            steps {
                sh 'docker build --target tester -t velos-api-test .'
            }
        }
        stage('Construire') {
            steps {
                sh 'docker build -t ${IMAGE}:${TAG} .'
            }
        }
        stage('Publier') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub', usernameVariable: 'DUSER', passwordVariable: 'DPASS')]) {
                    sh 'echo $DPASS | docker login -u $DUSER --password-stdin'
                    sh 'docker push ${IMAGE}:${TAG}'
                }
            }
        }
        stage('Déployer') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig-kind', variable: 'KUBECONFIG')]) {
                    sh 'kubectl set image deployment/api-deployment api=${IMAGE}:${TAG} --kubeconfig=$KUBECONFIG'
                    sh 'kubectl rollout status deployment/api-deployment --kubeconfig=$KUBECONFIG'
                }
            }
        }
    }
}
