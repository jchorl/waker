FROM python:3.7
LABEL maintainer "Josh Chorlton <josh@joshchorlton.com>"

RUN useradd -u 1000 -ms /bin/bash waker -G audio

RUN apt-get update && apt-get install -y \
    alsa-utils \
    vlc
ADD server/requirements.txt /
RUN pip install -r /requirements.txt

USER waker
WORKDIR /home/waker

ADD --chown=waker server /home/waker/
