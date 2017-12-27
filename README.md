# docker-alpine-pypy

[![Build Status](https://img.shields.io/travis/JayH5/docker-alpine-pypy/master.svg?style=flat-square)](https://travis-ci.org/JayH5/docker-alpine-pypy)
[![Docker Pulls](https://img.shields.io/docker/pulls/jamiehewland/alpine-pypy.svg?style=flat-square)](https://hub.docker.com/r/jamiehewland/alpine-pypy/)

> **Note:** As of PyPy 5.10.0, these images will only be available in one variety: a minimal image with no build tools. They will also track the latest Alpine Linux version available at the time that the included PyPy version was released. The Alpine version will be included in the image tag.

Docker images for [PyPy](http://pypy.org) running on [Alpine Linux](http://www.alpinelinux.org).

PyPy for Alpine Linux is built from [this](https://github.com/JayH5/alpine-pypy) repository. These are the associated Docker images that use that PyPy build.

These images seek to mimic the [official PyPy Docker images](https://hub.docker.com/_/pypy/) but are based on Alpine Linux instead of Debian for a smaller image size.

Built images are available from [Docker Hub](https://hub.docker.com/r/jamiehewland/alpine-pypy/).
