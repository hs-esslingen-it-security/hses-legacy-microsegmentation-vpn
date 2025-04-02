from scapy.all import rdpcap, wrpcap
from scapy.layers.inet import IP

def modify_pcap(input_file, output_file, new_dst_ip):
    # Read the pcap file
    packets = rdpcap(input_file)

    for packet in packets:
        if packet.haslayer(IP):
            packet[IP].dst = new_dst_ip
            # Recalculate the checksum after changing the IP address
            del packet[IP].chksum

    wrpcap(output_file, packets)

# Main function
if __name__ == "__main__":
    input_file = "unauthorized_rename.pcap"
    output_file = "unauthorized.pcap"
    modify_pcap(input_file, output_file, "192.168.1.50")
