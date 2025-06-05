#!/bin/bash
echo "Starting SCADA..."

#ip link set dev eth0 address 00:1d:9c:c6:72:e8

ip link set eth0 up
ip -4 addr show dev eth0 | awk '/inet / {print $2}' | while read ip; do ip addr del $ip dev eth0; done
ip addr add 192.168.1.100/28 dev eth0

ip route add 192.168.1.8/29 via 192.168.1.101
ip route add 192.168.1.16/29 via 192.168.1.102
ip route add 192.168.1.24/29 via 192.168.1.103
ip route add 192.168.1.32/28 via 192.168.1.104
ip route add 192.168.1.48/29 via 192.168.1.105
ip route add 192.168.1.56/29 via 192.168.1.106


# echo "SCADA is ready with MAC 00:1d:9c:c6:72:e8!"

# Custom startup commands
while true; do
    echo "SCADA running..."
    tcpdump -r /pcaps/dump.pcap -w- 'src 192.168.1.100' | tcpreplay -ieth0 - 
    sleep 30
done