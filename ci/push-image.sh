#!/usr/bin/env bash

echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin
docker push jason0722985179/explanation-ai-display:1.3
docker rmi jason0722985179/explanation-ai-display:1.3

