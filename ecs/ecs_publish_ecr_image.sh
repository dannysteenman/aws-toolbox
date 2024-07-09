#!/bin/bash

# This script builds a Docker image and publishes it to a given repository in the AWS ECR service
# Use the --help argument to check the full usage

set -e

AWS_PROFILE="default"
CLUSTER_NAME="qubec-cluster"
DOCKER_FILE="./Dockerfile"
TAG="latest"

usage() {
    cat <<EOF
Publish a script to Amazon Elastic Container Registry given a repository URL. The script assumes that the AWS CLI has already
been configured in the local shell, at least the default profile.

Usage
-----
./ecs_publish_ecr_image.sh --ecr-url ecr_repo_url [--dockerfile /path/to/dockerfile] [--profile <aws_profile>] [--tag <docker_image_tag>] [--help]

A short version of the commands is also available:
./ecs_publish_ecr_image.sh -e ecr_repo_url [-d /path/to/dockerfile] [-p <aws_profile>] [-t <docker_image_tag>] [-h]

Arguments
---------
The required --ecr-url argument takes a URL of valid repository in the AWS container registry (ECR)

The optional --dockerfile argument takes a path to a valid Dockerfile which can be used to build the Docker image
to send to AWS container registry.

The optional --profile argument takes as input an AWS CLI profile stored locally (see ~/.aws/config to see the
profiles currently available in your machine)
EOF
}

if ! command -v docker &>/dev/null; then
    echo "This script requires Docker to be installed and available in the shell PATH!"
    exit
fi

while [ "$1" != "" ]; do
    case $1 in
    -p | --profile)
        shift
        AWS_PROFILE="$1"
        ;;
    -d | --dockerfile)
        shift
        DOCKER_FILE="$1"
        ;;
    -e | --ecr-url)
        shift
        ECR_URL="$1"
        ;;
    -t | --tag)
        shift
        TAG="$1"
        ;;
    -h | --help)
        shift
        usage
        exit
        ;;
    esac
    shift
done

echo $ECR_URL

if [ -z $ECR_URL ]; then
    usage
    exit
fi

echo "Chosen AWS profile: $AWS_PROFILE"
echo "Chosen ECR repository address: $ECR_URL"
echo "Chosen Dockerfile to use for building the image: $DOCKER_FILE"

aws ecr --profile ${AWS_PROFILE} get-login-password | docker login --username AWS --password-stdin "${ECR_URL}"

docker build -t "$ECR_URL:$TAG" -f ${DOCKER_FILE} .
docker tag "$ECR_URL":"$TAG" "$ECR_URL":$TAG
docker push "$ECR_URL":$TAG
