FROM praekeltfoundation/alpine-buildpack-deps:3.4
LABEL maintainer "Jamie Hewland <jhewland@gmail.com>"

# ensure local pypy is preferred over distribution python
ENV PATH /usr/local/bin:$PATH

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8

ENV PYPY_VERSION 5.7.1
ENV PYPY_SHA256SUM ddfae2f9706c5327b102197ac61709b3a3529e0300578cc4f9df4dde5c783b96

# if this is called "PIP_VERSION", pip explodes with "ValueError: invalid truth value '<VERSION>'"
ENV PYTHON_PIP_VERSION 9.0.1

RUN set -ex; \
    apk add --no-cache --virtual .fetch-deps tar; \
    \
    wget -O pypy.tar.bz2 "https://github.com/JayH5/alpine-pypy/releases/download/2-$PYPY_VERSION/pypy2-v${PYPY_VERSION}-linux64.tar.bz2"; \
    echo "$PYPY_SHA256SUM *pypy.tar.bz2" | sha256sum -c; \
    tar -xjC /usr/local --strip-components=1 -f pypy.tar.bz2; \
    rm pypy.tar.bz2; \
    \
    runDeps="$( \
        scanelf --needed --nobanner --recursive /usr/local \
            | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
            | sort -u \
            | grep -v 'libpypy-c' \
    )"; \
    apk add --no-cache --virtual .pypy-rundeps $runDeps; \
    \
    apk del .fetch-deps

RUN set -ex; \
    \
    wget -O get-pip.py 'https://bootstrap.pypa.io/get-pip.py'; \
    \
    pypy get-pip.py \
        --disable-pip-version-check \
        --no-cache-dir \
        "pip==$PYTHON_PIP_VERSION" \
    ; \
    pip --version; \
    \
    rm -f get-pip.py

CMD ["pypy"]
