#!/bin/bash

docker rmi $(docker images -f "dangling=true" -q)
docker-compose stop app worker
docker-compose rm app worker --force

DOCKER_HUB_IMAGE="teeratachdocker/luna_manga_api"
docker pull $DOCKER_HUB_IMAGE
docker-compose up -d --build
