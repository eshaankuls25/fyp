#!/bin/bash
#
# Script to start docker container build
#

git clone https://github.com/Quantza/fyp ~/fyp/

cp ~/fyp/set/code/Dockerfiles/Dockerfile ~
sudo docker build -t set_box .



