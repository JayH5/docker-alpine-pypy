#!/usr/bin/env bash
set -e

cd "$VERSION"

# Parse the image name from the onbuild Dockerfile and add the variant
IMAGE="$(awk '$1 == "FROM" { print $2; exit }' onbuild/Dockerfile)${VARIANT:+-$VARIANT}"

# Build the image
docker build -t "$IMAGE" "${VARIANT:-.}"

# Build the onbuild image if we're building the standard image because the
# onbuild image is FROM it
if [[ -z "$VARIANT" ]]; then
  docker build -t "${IMAGE}-onbuild" onbuild
fi
