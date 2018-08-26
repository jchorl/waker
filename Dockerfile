FROM python:3.7
LABEL maintainer "Josh Chorlton <josh@joshchorlton.com>"

RUN apt-get update && apt-get install -y \
    vlc \
    pulseaudio

ADD . /waker
WORKDIR /waker
RUN pip install -r server/requirements.txt

ENV uid 1000
ENV gid 1000

# creates a waker user
RUN echo "waker:x:${uid}:${gid}:waker,,,:/waker:/bin/bash" >> /etc/passwd && \
    echo "waker:x:${uid}:" >> /etc/group && \
    mkdir /etc/sudoers.d && \
    echo "waker ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/waker && \
    chmod 0440 /etc/sudoers.d/waker && \
    chown ${uid}:${gid} /waker

USER waker
