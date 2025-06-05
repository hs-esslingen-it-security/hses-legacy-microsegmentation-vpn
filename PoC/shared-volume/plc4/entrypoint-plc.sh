#!/bin/bash
echo "Starting End Device 4..."

if [ -f "/pcaps/plc4-gw.pcap" ]; then
    echo "Rewritten pcap for PLC4 exists."
else
    tcpdump -r /pcaps/demo.pcap -w /pcaps/plc4.pcap 'src 192.168.1.40'
    tcprewrite --infile=/pcaps/plc4.pcap --outfile=/pcaps/plc4-gw.pcap --enet-dmac=00:1d:9c:00:00:04
fi

ip link set eth0 up
ip -4 addr show dev eth0 | awk '/inet / {print $2}' | while read ip; do ip addr del $ip dev eth0; done
ip addr add 192.168.1.40/28 dev eth0
ip route add default via 192.168.1.39

# Custom startup commands
while true; do
    echo "Device 4 running..."
    tcpdump -r /pcaps/plc4-gw.pcap -w- 'src 192.168.1.40' | tcpreplay -ieth0 - 
    sleep 30
done