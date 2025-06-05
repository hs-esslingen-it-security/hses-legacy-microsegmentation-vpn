#!/bin/bash
echo "Starting End Device 3..."

if [ -f "/pcaps/plc3-gw.pcap" ]; then
    echo "Rewritten pcap for PLC3 exists."
else
    tcpdump -r /pcaps/dump.pcap -w /pcaps/plc3.pcap 'src 192.168.1.30'
    tcprewrite --infile=/pcaps/plc3.pcap --outfile=/pcaps/plc3-gw.pcap --enet-dmac=00:1d:9c:00:00:03
fi

ip link set eth0 up
ip -4 addr show dev eth0 | awk '/inet / {print $2}' | while read ip; do ip addr del $ip dev eth0; done
ip addr add 192.168.1.30/29 dev eth0
ip route add default via 192.168.1.29

# Custom startup commands
while true; do
    echo "Device 3 running..."
    tcpdump -r /pcaps/plc3-gw.pcap -w- 'src 192.168.1.30' | tcpreplay -ieth0 - 
    sleep 30
done