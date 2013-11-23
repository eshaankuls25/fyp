#!/bin/bash
#
# Script to start docker container build
#

git clone https://github.com/Quantza/fyp ~/fyp/
mkdir ~/docker_build/ && cd ~/docker_build/
cp ~/fyp/set/code/Dockerfiles/Dockerfile .
sudo docker build -t set_box .



