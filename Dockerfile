FROM ubuntu:jammy
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
  apt-transport-https \
  build-essential \
  ca-certificates \
  curl \
  git \
  python3 \
  python3-pip \
  python3-requests \
  python3-requests-cache \
  && pip install pydantic-ai quart quart_cors \
  && update-ca-certificates \
  && rm -rf /var/lib/apt/lists/* \
  && mkdir -p /git/homeassistant
RUN git clone https://github.com/tuxthepenguin84/homeassistant.git /git/homeassistant
ADD params.json /git/homeassistant/params.json
ADD ha.json /git/homeassistant/ha.json
EXPOSE 5000/tcp
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --start-interval=5s --retries=3 \
  CMD curl --fail --connect-timeout 5 http://localhost:5000/health || exit 1
WORKDIR /git/homeassistant
ENTRYPOINT ["/usr/bin/python3", "-u", "/git/homeassistant/api.py"]