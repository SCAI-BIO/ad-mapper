#!/bin/groovy
pipeline {
    agent any
    triggers {
        pollSCM('H/10 * * * 1-5')
    }
    environment {
        WORK_DIR=pwd()
        BACKEND_IMAGE_REPO="docker.arty.scai.fraunhofer.de/ad-mapper-backend"
        FRONTEND_IMAGE_REPO="docker.arty.scai.fraunhofer.de/ad-mapper-frontend"
        IMAGE_VERSION="latest"
        BUILD_NAME="ADmapper"
        K8S_DEPLOYMENT="ad-mapper-ad-mapper-deployment"
    }
    stages {
        stage ('Build - Backend Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'bio-services-arty', passwordVariable: 'password', usernameVariable: 'user')]){
                       sh "docker login docker.arty.scai.fraunhofer.de -u ${user} -p ${password}"
                       sh "cd backend/"
                       sh "docker image build . -t ${BACKEND_IMAGE_REPO}:${IMAGE_VERSION}"
                       sh "docker image push ${BACKEND_IMAGE_REPO}:${IMAGE_VERSION}"
                       sh "cd .."
                }
            }
        }

        stage ('Build - Frontend Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'bio-services-arty', passwordVariable: 'password', usernameVariable: 'user')]){
                       sh "docker login docker.arty.scai.fraunhofer.de -u ${user} -p ${password}"
                       sh "cd frontend/"
                       sh "docker image build . -t ${FRONTEND_IMAGE_REPO}:${IMAGE_VERSION}"
                       sh "docker image push ${FRONTEND_IMAGE_REPO}:${IMAGE_VERSION}"
                       sh "cd .."
                }
            }
        }

        stage ('Deploy - k8s') {
            steps {
                withKubeConfig(clusterName : "kubernetes", contextName:"bio", namespace: "bio", credentialsId: 'k8s-bioservices', serverUrl: "https://193.175.167.109:6443"){
                       sh "kubectl rollout restart deployment ${K8S_DEPLOYMENT}"
                }
            }
        }
    }
    post {
        success {
            echo "Successfully updated image and deployed in k8s";
        }
       failure {
            echo "Pipeline failed";
       	    deleteDir()
        }
    }
}
