ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:3.19
FROM ${BUILD_FROM}

RUN apk add --no-cache \
    wireless-tools \
    iw \
    ethtool \
    busybox-extras

COPY run.sh /run.sh
RUN chmod +x /run.sh

CMD ["/run.sh"]
