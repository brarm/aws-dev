#!/bin/bash

if [[ ! -v $1 ]]
then
	echo 'Specify an ECR name'
	exit
fi

sudo service docker start
docker build --no-cache -t $1 .
$(aws ecr get-login --no-include-email)
ecr_repo_url=$(aws ecr describe-repositories --repository-names $1 --query "repositories[0].repositoryUri")
echo $ecr_repo_url
docker tag wb-app/docker-images:latest "$ecr_repo_url:latest"
docker push "$ecr_repo_url:latest"

sleep 5
aws ecs update-service --force-new-deployment --service wb-fargate-service --cluster wb-fargate-cluster
