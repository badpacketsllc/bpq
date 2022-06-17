ARG PYTHON_VERSION=3.9
ARG VERSION=latest
FROM docker.io/python:${PYTHON_VERSION}-alpine

LABEL org.opencontainers.image.authors="Mathew Woodyard" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.licenses="Apache-2.0" \
      org.opencontainers.image.title="bpq" \
      org.opencontainers.image.description="Tools for interacting with Bad Packets CTI API." \
      org.opencontainers.image.base.name="docker.io/python:${PYTHON_VERSION}-alpine"

WORKDIR /app

RUN adduser --disabled-password bp-api-user bp-api-user
USER bp-api-user
COPY --chown=bp-api-user:bp-api-user --chmod=0440 VERSION /app
COPY --chown=bp-api-user:bp-api-user --chmod=0440 bpq/ /app/bpq/

ENTRYPOINT ["/usr/local/bin/python3", "-m", "bpq.cli"]
CMD []
