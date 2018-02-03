FROM alpine:3.7
LABEL maintainer "Jamie Hewland <jhewland@gmail.com>"

# ensure local pypy is preferred over distribution python
ENV PATH /usr/local/bin:$PATH

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8

# install ca-certificates so that HTTPS works consistently
# the other runtime dependencies for PyPy are installed later
RUN apk add --no-cache ca-certificates

ENV PYPY_VERSION 5.10.0
ENV PYPY_SHA256SUM 3c23060bd45e48ddf87f7f1eaa31485d9b358c1d7e1fa025977e05addf4ce086

# if this is called "PIP_VERSION", pip explodes with "ValueError: invalid truth value '<VERSION>'"
ENV PYTHON_PIP_VERSION 9.0.1

RUN set -ex; \
    apk add --no-cache --virtual .fetch-deps \
        libressl \
        tar \
        xz \
    ; \
    \
    filename="pypy2-v${PYPY_VERSION}-linux64-alpine$(cut -d '.' -f 1,2 /etc/alpine-release).tar.bz2"; \
    wget -O pypy.tar.bz2 "https://github.com/JayH5/alpine-pypy/releases/download/2-$PYPY_VERSION/$filename"; \
    \
    echo "$PYPY_SHA256SUM *pypy.tar.bz2" | sha256sum -c -; \
    tar -xjC /usr/local --strip-components=1 -f pypy.tar.bz2; \
    rm pypy.tar.bz2; \
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
    wget -O get-pip.py 'https://bootstrap.pypa.io/get-pip.py'; \
    \
    pypy get-pip.py \
        --disable-pip-version-check \
        --no-cache-dir \
        "pip==$PYTHON_PIP_VERSION" \
    ; \
    pip --version; \
    \
    rm -f get-pip.py; \
    \
    apk del .fetch-deps

CMD ["pypy"]
