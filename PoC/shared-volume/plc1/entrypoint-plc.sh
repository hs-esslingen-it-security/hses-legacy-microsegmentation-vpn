#!/bin/bash
echo "Starting End Device 1..."

if [ -f "/pcaps/plc1-gw.pcap" ]; then
    echo "Rewritten pcap for PLC1 exists."
else
    tcpdump -r /pcaps/demo.pcap -w /pcaps/plc1.pcap 'src 192.168.1.10'
    tcprewrite --infile=/pcaps/plc1.pcap --outfile=/pcaps/plc1-gw.pcap --enet-dmac=00:1d:9c:00:00:01
fi

ip link set eth0 up
ip -4 addr show dev eth0 | awk '/inet / {print $2}' | while read ip; do ip addr del $ip dev eth0; done
ip addr add 192.168.1.10/29 dev eth0
ip route add default via 192.168.1.11

# Custom startup commands
while true; do
    echo "Device 1 running..."
    tcpdump -r /pcaps/plc1-gw.pcap -w- 'src 192.168.1.10' | tcpreplay -ieth0 - 
    sleep 30
done