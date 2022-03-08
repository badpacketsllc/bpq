ARG PYTHON_VERSION=39
ARG VERSION=latest
FROM registry.access.redhat.com/ubi8/python-${PYTHON_VERSION}

LABEL org.opencontainers.image.authors="Mathew Woodyard" \
      org.opencontainers.image.licenses="GPL-3.0-or-later" \
      org.opencontainers.image.vendor="Bad Packets, LLC" \
      org.opencontainers.image.title="bpq" \
      org.opencontainers.image.description="Tools for interacting with Bad Packets CTI API." \
      org.opencontainers.image.base.name="registry.access.redhat.com/ubi8/python-${PYTHON_VERSION}"

WORKDIR /opt/app-root/src

COPY --chmod=0440 VERSION /opt/app-root/src
COPY --chmod=0440 bpq/ /opt/app-root/src/bpq/

ENTRYPOINT ["/opt/app-root/bin/python3", "-m", "bpq.cli"]
CMD []
