# docker-alpine-pypy

[![Build Status](https://img.shields.io/travis/JayH5/docker-alpine-pypy/develop.svg)](https://travis-ci.org/JayH5/docker-alpine-pypy)

Docker images for [PyPy](http://pypy.org) running on [Alpine Linux](http://www.alpinelinux.org).

PyPy for Alpine Linux is built from [this](https://github.com/JayH5/alpine-pypy) repository. These are the associated Docker images to use that PyPy.

These images seek to mimic the [official PyPy Docker images](https://hub.docker.com/_/pypy/) but are based on Alpine Linux instead of Debian for a smaller image size.

Built images are available from [Docker Hub](https://hub.docker.com/r/jamiehewland/alpine-pypy/).

### Building the images
The images are automatically built by Travis CI using the [`build.sh`](build.sh) script and pushed to Docker Hub using the [`deploy.sh`](deploy.sh) script.

You can build (and deploy) the images locally by recreating what Travis does.
```bash
export VERSION=2 VARIANT=slim
./build.sh

export REGISTRY_USER=myuser REGISTRY_PASS="mysecretpassw0rd"
./deploy.sh
```
