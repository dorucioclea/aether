#!/usr/bin/env bash
set -e

IMAGE_REPO='ehealthafrica'

export APPS=( kernel odk )

for APP in "${APPS[@]}"
do
	VERSION=`cat $APP/VERSION`
	echo "version: $VERSION"

  AETHER_APP="aether-${APP}"
  echo "Building Docker image ${IMAGE_REPO}/${AETHER_APP}:${VERSION}"
  docker-compose build --build-args GIT_REVISION=$TRAVIS_COMMIT $APP
  docker tag ${AETHER_APP} "${IMAGE_REPO}/${AETHER_APP}:${VERSION}"
  docker tag ${AETHER_APP} "${IMAGE_REPO}/${AETHER_APP}:latest"
  echo "Pushing Docker image ${IMAGE_REPO}/${AETHER_APP}:${VERSION}"
  docker push "${IMAGE_REPO}/${AETHER_APP}:${VERSION}"
  docker push "${IMAGE_REPO}/${AETHER_APP}:latest"
done
