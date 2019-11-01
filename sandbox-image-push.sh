#!/bin/bash

sudo service docker start
docker build --no-cache -t wb-app/docker-images .
$(aws ecr get-login --no-include-email)
ecr_repo_url=$(aws ecr describe-repositories --repository-names wb-app/docker-images --query "repositories[0].repositoryUri")
echo $ecr_repo_url
docker tag wb-app/docker-images:latest "$ecr_repo_url:latest"
docker push "$ecr_repo_url:latest"

sleep 5
aws ecs update-service --force-new-deployment --service wb-fargate-service --cluster wb-fargate-cluster
