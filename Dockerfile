FROM python:3.7
LABEL maintainer "Josh Chorlton <josh@joshchorlton.com>"

RUN apt-get update && apt-get install -y \
    alsa-utils \
    vlc

ADD . /waker
WORKDIR /waker
RUN pip install -r server/requirements.txt

RUN groupadd -g 1000 waker && useradd -u 1000 -d /waker --no-log-init -r -G audio -g 1000 waker

USER waker
