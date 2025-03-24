#!/bin/bash

# Input and output pcap file paths
INPUT_PCAP="Dec2019_00000_20191206100500.pcap"
OUTPUT_PCAP="filtered_plc_packets.pcap"
OUTPUT_PCAP_50="filtered_plc_packets_50.pcap"

# SWaT IP addresses
IPS=(
    "192.168.1.10"
    "192.168.1.20"
    "192.168.1.30"
    "192.168.1.40"
    "192.168.1.50"
    "192.168.1.60"
    "192.168.1.100"
)

# Construct the TShark display filter
SRC_FILTER=""
DST_FILTER=""

for IP in "${IPS[@]}"; do
    if [ -n "$SRC_FILTER" ]; then
        SRC_FILTER+=" || "
        DST_FILTER+=" || "
    fi
    SRC_FILTER+="ip.src==$IP"
    DST_FILTER+="ip.dst==$IP"
done

DISPLAY_FILTER="($SRC_FILTER) && ($DST_FILTER)"

echo "Applying filter: $DISPLAY_FILTER"

# tshark to filter and save the packets
tshark -r "$INPUT_PCAP" -Y "$DISPLAY_FILTER" -w "$OUTPUT_PCAP"

# tshark to filter and save first 50,000 packets
tshark -r "$OUTPUT_PCAP" -c 50000 -w "$OUTPUT_PCAP_50"
echo "Filtered packets saved to $OUTPUT_PCAP_50"