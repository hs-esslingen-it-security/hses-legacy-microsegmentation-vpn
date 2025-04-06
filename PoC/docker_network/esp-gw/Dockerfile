FROM ubuntu:latest

RUN apt update && apt install -y \
    wireguard \
    iptables \
    python3 \
    python3-pip \
    tcpdump \
    tcpreplay \
    iproute2 \
    sudo \
    nano \
    vim \
    bridge-utils \
    iputils-ping
    
RUN ln -s /usr/bin/python3 /usr/bin/python

RUN modprobe wireguard || true

COPY requirements.txt /opt/requirements.txt
RUN pip3 install --no-cache-dir --break-system-packages -r /opt/requirements.txt

WORKDIR /data
