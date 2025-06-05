FROM ubuntu:latest

RUN apt update && apt install -y \
    python3 \
    python3-pip \
    tcpdump \
    tcpreplay \
    iproute2 \
    sudo  \
    nano \
    vim \
    iputils-ping
    
RUN ln -s /usr/bin/python3 /usr/bin/python

WORKDIR /data
