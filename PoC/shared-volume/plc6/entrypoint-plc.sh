#!/bin/bash
echo "Starting End Device 6..."

if [ -f "/pcaps/plc6-gw.pcap" ]; then
    echo "Rewritten pcap for PLC6 exists."
else
    tcpdump -r /pcaps/dump.pcap -w /pcaps/plc6.pcap 'src 192.168.1.60'
    tcprewrite --infile=/pcaps/plc6.pcap --outfile=/pcaps/plc6-gw.pcap --enet-dmac=00:1d:9c:00:00:06
    #tcprewrite --infile=/pcaps/unauthorized.pcap --outfile=/pcaps/unauthorized-gw.pcap --enet-dmac=00:1d:9c:00:00:06
fi

ip link set eth0 up
ip -4 addr show dev eth0 | awk '/inet / {print $2}' | while read ip; do ip addr del $ip dev eth0; done
ip addr add 192.168.1.60/29 dev eth0
ip route add default via 192.168.1.61

# Custom startup commands
while true; do
    echo "Device 6 running..."
    tcpdump -r /pcaps/plc6-gw.pcap -w- 'src 192.168.1.60' | tcpreplay -ieth0 - 
    tcpdump -r /pcaps/unauthorized-gw.pcap -w- 'src 192.168.1.60' | tcpreplay -ieth0 - 
    sleep 30
done