#!/usr/bin/env bash

if [ -z "$1" ]
  then
    echo "No input parameters supplied"
    exit 1
fi

IMAGE_NAME=reljicd/komoot_challenge
echo -e "\nSet docker image name as ${IMAGE_NAME}\n"

echo -e "\nStop running Docker containers with image name ${IMAGE_NAME}...\n"
sudo docker stop $(docker ps -a | grep ${IMAGE_NAME} | awk '{print $1}')

echo -e "\nDocker build image with name ${IMAGE_NAME}...\n"
sudo docker build -t ${IMAGE_NAME} -f docker/Dockerfile .

echo -e "\nStart Docker container of the image ${IMAGE_NAME}...\n"
sudo docker run --rm -i ${IMAGE_NAME} $@