#!/bin/bash
set -o allexport

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/..

if [ -e .env ]; then
	source .env
fi
echo $HELLOTEST_DOCKER_IMAGE_LOCAL

docker build -t $HELLOTEST_DOCKER_IMAGE_LOCAL:$HELLOTEST_IMAGE_VERSION . 
