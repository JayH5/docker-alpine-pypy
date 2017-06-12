FROM alpine:3.4
LABEL maintainer "Jamie Hewland <jhewland@gmail.com>"

# ensure local pypy is preferred over distribution python
ENV PATH /usr/local/bin:$PATH

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8

# install ca-certificates so that HTTPS works consistently
# the other runtime dependencies for PyPy are installed later
RUN apk add --no-cache ca-certificates

ENV PYPY_VERSION 5.8.0
ENV PYPY_SHA256SUM 7e41554cd0fbf7d569bbc5a42abc29814ad504f4a53ab536bd0de98b400fb8cb

# if this is called "PIP_VERSION", pip explodes with "ValueError: invalid truth value '<VERSION>'"
ENV PYTHON_PIP_VERSION 9.0.1

RUN set -ex; \
    apk add --no-cache --virtual .fetch-deps \
        openssl \
        tar \
        xz \
    ; \
    \
    wget -O pypy.tar.bz2 "https://github.com/JayH5/alpine-pypy/releases/download/3-$PYPY_VERSION/pypy3-v${PYPY_VERSION}-linux64.tar.bz2"; \
    echo "$PYPY_SHA256SUM *pypy.tar.bz2" | sha256sum -c -; \
    tar -xjC /usr/local --strip-components=1 -f pypy.tar.bz2; \
    rm pypy.tar.bz2; \
    \
    runDeps="$( \
        scanelf --needed --nobanner --recursive /usr/local \
            | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
            | sort -u \
            | grep -v 'libpypy3-c' \
    )"; \
    apk add --no-cache --virtual .pypy-rundeps $runDeps; \
    \
    wget -O get-pip.py 'https://bootstrap.pypa.io/get-pip.py'; \
    \
    pypy3 get-pip.py \
        --disable-pip-version-check \
        --no-cache-dir \
        "pip==$PYTHON_PIP_VERSION" \
    ; \
    pip --version; \
    \
    rm -f get-pip.py; \
    \
    apk del .fetch-deps

CMD ["pypy3"]
