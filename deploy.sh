#!/usr/bin/env bash
set -e

cd "$VERSION"

# Parse the image name from the onbuild Dockerfile and add the variant
IMAGE="$(awk '$1 == "FROM" { print $2; exit }' onbuild/Dockerfile)${VARIANT:+-$VARIANT}"

# Parse the version of PyPy from the standard Dockerfile
PYPY_VERSION="$(sed -n 's/.*PYPY_VERSION="\(.*\)".*/\1/p' Dockerfile)"

function version_tags {
  local image="$1"; shift
  local version="$1"; shift

  local image_tag="${image##*:}"
  local tags=("$image_tag")
  IFS=- read -r tag_start tag_end <<< "$image_tag"

  # Generate all variations of version (e.g. 5.3.1, 5.3, 5) and insert into tag
  while [[ -n "$version" ]]; do
    tags+=("$tag_start-$version${tag_end:+-$tag_end}")
    version="$(echo "$version" | sed -E 's/[.-]?[[:alnum:]]+$//')"
  done

  echo "${tags[@]}"
}

function deploy {
  local image="$1"; shift

  local tags="$(version_tags "$image" "$PYPY_VERSION")"
  docker-ci-deploy --tag $tags -- "$image"
}

# Login to Docker Hub
docker login -u "$REGISTRY_USER" -p "$REGISTRY_PASS"

# Deploy the image
deploy "$IMAGE"

# Deploy the onbuild image if we're building the standard image
if [[ -z "$VARIANT" ]]; then
  deploy "$IMAGE-onbuild"
fi
