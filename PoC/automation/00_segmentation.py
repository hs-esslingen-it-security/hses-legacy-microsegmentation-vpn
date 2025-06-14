
import subprocess
import logging
import pandas as pd
import argparse
from helper.micro_segmentation import *
from helper.firewall_rules_generation import generate_firewall_rules_host_level, generate_firewall_rules_application_level

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

gw_to_ip_map = {"esp-gw1": "192.168.1.10",
                "esp-gw2": "192.168.1.20",
                "esp-gw3": "192.168.1.30",
                "esp-gw4": "192.168.1.40",
                "esp-gw5": "192.168.1.50",
                "esp-gw6": "192.168.1.60",
                "scada":   "192.168.1.100"}


def capture(filename: str = "demo", container: str = "esp-gw6", count: int = 1000):
    subprocess.run(f'docker exec {container} tcpdump -w /pcaps/{filename}.pcap -c {count}'.split(' '), check=True)

def filter_pcap(filename: str = "demo"):
    from nfstream import NFStreamer, NFPlugin
    from dataclasses import dataclass, field
    
    class EthernetIP(NFPlugin):
        def on_init(self, packet, flow):
            # Check if the packet is UDP and the port is 2222
            return packet.protocol == 17 and packet.dst_port == 2222 #  I/O over EtherNet/IP
        def on_expire(self, flow):
            if EthernetIP:
                flow.application_name = "EthernetIP"  # Override app name
                flow.application_category_name = "Network"  # Override app category

    my_streamer = NFStreamer(source=f"../shared-volume/shared-pcaps/{filename}.pcap", udps=EthernetIP(volatile=True))
    total_flows = my_streamer.to_csv(path=f"../shared-volume/shared-pcaps/{filename}.csv")
    return total_flows


def main():
    parser = argparse.ArgumentParser(description="ESP Microsegmentation and VPN Configurator. Example use: python3 00_segmentation.py --gateways esp-gw5 esp-gw6 --segmentation --granularity device --vpn")

    parser.add_argument(
        "--gateways",
        nargs="+",
        default=["esp-gw1", "esp-gw2", "esp-gw5"],
        help="List of gateway container names (default: esp-gw1, esp-gw2, esp-gw5)"
    )

    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Capture and filter new pcap file instead of using cached CSV (requires NFStream support)"
    )

    parser.add_argument(
        "--segmentation",
        action="store_true",
        help="Enable micro-segmentation (firewall rule generation and application)"
    )

    parser.add_argument(
        "--vpn",
        action="store_true",
        help="Enable VPN tunnel setup"
    )

    parser.add_argument(
        "--csv",
        default="demo.csv",
        help="CSV file traffic flows for analysis (default: 'demo.csv')"
    )

    parser.add_argument(
        "--granularity",
        choices=["device", "stream"],
        default="stream",
        help="Segmentation rule granularity: 'device' for host-level, 'stream' for application-level (default: 'stream')"
    )

    args = parser.parse_args()

    GATEWAYS = args.gateways
    FILENAME = args.csv
    REFRESH = args.refresh
    SEGMENTATION = args.segmentation
    VPN = args.vpn
    GRANULARITY = args.granularity

    IPS = [gw_to_ip_map[gw] for gw in GATEWAYS]
    REVERSE_MAP = {gw_to_ip_map[gw]: gw for gw in GATEWAYS}


    #if REFRESH: # requires NFStream support, due to reproducibility issues outsourced for now
        #capture(filename=FILENAME)
        #filter_pcap(filename=FILENAME)

    df_flows = pd.read_csv(f"../shared-volume/shared-pcaps/{FILENAME}", sep=',')

    if SEGMENTATION:
        firewall_config = {}
        for gw in GATEWAYS:
            if GRANULARITY == "device":
                firewall_config[gw] = generate_firewall_rules_host_level(gw_to_ip_map[gw], df_flows)
            else:
                firewall_config[gw] = generate_firewall_rules_application_level(gw_to_ip_map[gw], df_flows)

        for gw in firewall_config:
            logging.info(f"GW: {gw} ({gw_to_ip_map[gw]})")
            for rule in firewall_config[gw]:
                subprocess.run(f'docker exec {gw} {rule}'.split(' '), check=True)
                logging.info(f"    + {rule}")
            logging.info("\n\n")

    if VPN:
        from helper.micro_segmentation import host_level_segmentation
        vpn_tunnels = []
        public_keys = {}
        for gw in GATEWAYS:
            output = subprocess.run(['./helper/wireguard_00.sh', f'{gw}'], capture_output=True, text=True).stdout.strip()
            print(f"Output for {gw}: {output}")
            public_keys[gw] = output.split("________________")[1].strip()
            communication = host_level_segmentation(gw_to_ip_map[gw], df_flows)
            for communication_partner in communication["ip"]:
                if communication_partner in IPS:
                    if [gw_to_ip_map[gw], communication_partner] not in vpn_tunnels and [communication_partner, gw_to_ip_map[gw]] not in vpn_tunnels:
                        vpn_tunnels.append([gw_to_ip_map[gw], communication_partner])
        print(public_keys)
        per_tunnel_config = []
        for tunnel in vpn_tunnels:
            GW1 = REVERSE_MAP[tunnel[0]]
            GW2 = REVERSE_MAP[tunnel[1]]
            per_tunnel_config.append([GW1, GW2, f'{GW1.replace("esp-gw", "")}', f'{GW2.replace("esp-gw", "")}', public_keys[GW1], public_keys[GW2]])
        subprocess.run(['./helper/wireguard_01.sh', 
                        ','.join(['__'.join(vpn_tunnel) for vpn_tunnel in per_tunnel_config])], check=True)
 

if __name__ == "__main__":
    main()