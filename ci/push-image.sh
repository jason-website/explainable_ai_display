#!/usr/bin/env bash
USER_NAME=$DOCKERHUB_USR
USER_PASSWORD=$DOCKERHUB_PSW

docker login -u USER_NAME -p USER_PASSWORD
docker push jason0722985179/explanation-ai-display:1.3
docker rmi jason0722985179/explanation-ai-display:1.3
