#!/bin/bash
################################################################################
#
# Builder for new version-tagged docker images
#
# Builds and tags as latest as well as most recent git tag. Optionally pushes to 
# Docker hub if flag is passed.
#
################################################################################
DOCKER_REPO=halpoins
IMAGE_NAME=wmata_pmt
GIT_TAG=$(git describe --tags --abbrev=0)
APP_VERSION=${GIT_TAG:-dev}

usage () {
	cat <<USAGE

Usage: $0 [OPTIONS]

Options:
	-p, --push: 	Push the resulting image tags to Docker Hub

USAGE
	exit 1
}

build_image () {
	docker build \
	  -t "$DOCKER_REPO/$IMAGE_NAME:$APP_VERSION" \
	  -t "$DOCKER_REPO/$IMAGE_NAME:latest" \
	  .
  }

push_image () {
	for tag in "$APP_VERSION" "latest"
	do
		docker push "$DOCKER_REPO/$IMAGE_NAME:$tag"
	done
}

PUSH=false
while [ "$1" != "" ]; do
	case $1 in
	-p | --push)
		PUSH=true
		;;
	-h | --help)
		usage
		exit 1
		;;
	esac
	shift
done

build_image
if [ $PUSH == true ]; then
	push_image
fi
