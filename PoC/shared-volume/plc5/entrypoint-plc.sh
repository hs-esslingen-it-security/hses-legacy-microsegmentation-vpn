#!/bin/bash
echo "Starting End Device 5..."

if [ -f "/pcaps/plc5-gw.pcap" ]; then
    echo "Rewritten pcap for PLC5 exists."
else
    tcpdump -r /pcaps/dump.pcap -w /pcaps/plc5.pcap 'src 192.168.1.50'
    tcprewrite --infile=/pcaps/plc5.pcap --outfile=/pcaps/plc5-gw.pcap --enet-dmac=00:1d:9c:00:00:05
fi

ip link set eth0 up
ip -4 addr show dev eth0 | awk '/inet / {print $2}' | while read ip; do ip addr del $ip dev eth0; done
ip addr add 192.168.1.50/29 dev eth0
ip route add default via 192.168.1.51

# Custom startup commands
while true; do
    echo "Device 5 running..."
    tcpdump -r /pcaps/plc5-gw.pcap -w- 'src 192.168.1.50' | tcpreplay -ieth0 - 
    sleep 30
done