#!/bin/bash
echo "Starting End Device 2..."

if [ -f "/pcaps/plc2-gw.pcap" ]; then
    echo "Rewritten pcap for PLC2 exists."
else
    tcpdump -r /pcaps/dump.pcap -w /pcaps/plc2.pcap 'src 192.168.1.20'
    tcprewrite --infile=/pcaps/plc2.pcap --outfile=/pcaps/plc2-gw.pcap --enet-dmac=00:1d:9c:00:00:02
fi

ip link set eth0 up
ip -4 addr show dev eth0 | awk '/inet / {print $2}' | while read ip; do ip addr del $ip dev eth0; done
ip addr add 192.168.1.20/29 dev eth0
ip route add default via 192.168.1.21

# Custom startup commands
while true; do
    echo "Device 2 running..."
    tcpdump -r /pcaps/plc2-gw.pcap -w- 'src 192.168.1.20' | tcpreplay -ieth0 - 
    sleep 30
done