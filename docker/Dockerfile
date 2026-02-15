FROM ubuntu:24.04

LABEL maintainer="GoPro Overlay Dashboards <gopro-overlay@time4tea.net>"
ENV PATH=$PATH:/usr/bin


RUN apt update && apt install -y curl gnupg unzip fonts-noto fonts-roboto python3.12 ffmpeg sudo libcairo-dev

WORKDIR /
RUN apt install -y python3.12-venv
RUN python3.12 -mvenv venv
RUN /venv/bin/python3.12 -m pip install --upgrade pip

RUN apt install -y gcc
RUN apt install -y python3.12-dev libcairo2-dev pkg-config
RUN /venv/bin/pip install pycairo==1.23.0

RUN apt install -y libnvidia-decode-535-server libnvidia-encode-535-server
ARG GOPRO_OVERLAY_VERSION
RUN /venv/bin/pip install gopro-overlay==${GOPRO_OVERLAY_VERSION}

VOLUME /work
WORKDIR /work

COPY entrypoint.sh /

ENTRYPOINT [ "/entrypoint.sh" ]

