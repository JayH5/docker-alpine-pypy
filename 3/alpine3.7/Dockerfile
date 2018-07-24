FROM alpine:3.7
LABEL maintainer "Jamie Hewland <jhewland@gmail.com>"

# ensure local pypy is preferred over distribution python
ENV PATH /usr/local/bin:$PATH

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8

ENV PYPY_VERSION 6.0.0
ENV PYPY_SHA256SUM d20aa65d203dcaf5a6934431800d5e3739273702f8f24f8f900d656b0bb8a011

RUN set -ex; \
    apk add --no-cache --virtual .fetch-deps \
        tar \
        xz \
    ; \
    \
    filename="pypy3-v${PYPY_VERSION}-linux64-alpine$(cut -d '.' -f 1,2 /etc/alpine-release).tar.bz2"; \
    wget -O pypy.tar.bz2 "https://github.com/JayH5/alpine-pypy/releases/download/3-$PYPY_VERSION/$filename"; \
    \
    echo "$PYPY_SHA256SUM *pypy.tar.bz2" | sha256sum -c -; \
    tar -xjC /usr/local --strip-components=1 -f pypy.tar.bz2; \
    find /usr/local/lib-python -depth -type d -a \( -name test -o -name tests \) -exec rm -rf '{}' +; \
    rm pypy.tar.bz2; \
    apk del .fetch-deps; \
    \
    runDeps="$( \
        scanelf --needed --nobanner --format '%n#p' --recursive /usr/local \
            | tr ',' '\n' \
            | sort -u \
            | while read sofile; do \
                if [ ! -e "/usr/local/lib/$sofile" ] && [ ! -e "/usr/local/bin/$sofile" ]; then \
                    echo "so:$sofile"; \
                fi \
            done \
    )"; \
    apk add --no-cache --virtual .pypy-rundeps $runDeps; \
    \
    pypy3 --version

# if this is called "PIP_VERSION", pip explodes with "ValueError: invalid truth value '<VERSION>'"
ENV PYTHON_PIP_VERSION 18.0

RUN set -ex; \
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
    rm -f get-pip.py

CMD ["pypy3"]
