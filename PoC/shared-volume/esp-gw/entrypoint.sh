#!/bin/bash

# Create a bridge
ip link add br0 type bridge
ip link set br0 up

# Get the container PID
SWITCH_PID=$(cat /proc/1/cpuset | cut -d'/' -f3)

# Attach veth interfaces to the bridge
ip link set eth0 up
ip link set eth1 up
ip link set eth0 master br0
ip link set eth1 master br0

# Enable forwarding
echo 1 > /proc/sys/net/ipv4/ip_forward

# Custom startup commands
while true; do
    echo "Gateway running..."
    sleep 10
done