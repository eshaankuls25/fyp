#!/bin/bash
#
# Script to start docker container build
#

DOCKER_BUILD_PATH=~/docker_build/
DOCKERFILE=~/fyp/set/code/Dockerfiles/Dockerfile
GIT_PROJECT_PATH=~/fyp/

if [ -d "$GIT_PROJECT_PATH" ]; then
rm -rf $GIT_PROJECT_PATH
fi

if [ ! -d "$DOCKER_BUILD_PATH" ]; then
mkdir $DOCKER_BUILD_PATH
fi

git clone https://github.com/Quantza/fyp $GIT_PROJECT_PATH

cd $DOCKER_BUILD_PATH
cp $DOCKERFILE .

sudo docker build -t set_box .



