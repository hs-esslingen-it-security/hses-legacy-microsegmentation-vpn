#!/bin/bash
echo "Starting GW 3..."

ip link set dev eth0 address 00:1d:9c:00:00:03 # tcprewrite

ip link set eth0 up
ip link set eth1 up
ip -4 addr show dev eth0 | awk '/inet / {print $2}' | while read ip; do ip addr del $ip dev eth0; done
ip -4 addr show dev eth1 | awk '/inet / {print $2}' | while read ip; do ip addr del $ip dev eth1; done
ip addr add 192.168.1.29/29 dev eth0
ip addr add 192.168.1.103/28 dev eth1

ip route add 192.168.1.8/29 via 192.168.1.101
ip route add 192.168.1.16/29 via 192.168.1.102
ip route add 192.168.1.24/29 via 192.168.1.103
ip route add 192.168.1.32/28 via 192.168.1.104
ip route add 192.168.1.48/29 via 192.168.1.105
ip route add 192.168.1.56/29 via 192.168.1.106

sysctl -w net.ipv4.ip_forward=1

# Custom startup commands
while true; do
    echo "GW 3 running..."
    sleep 10
done