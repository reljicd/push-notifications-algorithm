#!/usr/bin/env bash

if [ -z "$1" ]
  then
    echo "No input path supplied"
    exit 1
fi

INPUT_CSV_PATH=$1

IMAGE_NAME=reljicd/komoot_challenge
echo -e "\nSet docker image name as ${IMAGE_NAME}\n"

echo -e "\nStop running Docker containers with image name ${IMAGE_NAME}...\n"
docker stop $(docker ps -a | grep ${IMAGE_NAME} | awk '{print $1}')

echo -e "\nDocker build image with name ${IMAGE_NAME}...\n"
docker build -t ${IMAGE_NAME} -f docker/Dockerfile .

echo -e "\nStart Docker container of the image ${IMAGE_NAME}...\n"
docker run --rm -i ${IMAGE_NAME} notifications_processor/main.py --events_csv_path=INPUT_CSV_PATH --print_to_stdout=True