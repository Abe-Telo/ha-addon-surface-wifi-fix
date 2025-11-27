ARG BUILD_FROM=ghcr.io/home-assistant/{arch}-base:3.19
FROM ${BUILD_FROM}

RUN apk add --no-cache \
    wireless-tools \
    iw \
    ethtool \
    jq \
    busybox-extras

COPY run.sh /run.sh
RUN chmod +x /run.sh

CMD ["/run.sh"]
