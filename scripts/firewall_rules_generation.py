import pandas as pd
import logging
from micro_segmentation import *
from pyroute2.netfilter.iptables import IPTables

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

########################
# firewall rule handling
########################

def apply_rule(chain: str, protocol: str, src_ip: str, dst_ip: str, src_port: str, dst_port: str):
    """
    Adds an iptables rule if it doesn't already exist.
    """
    try:
        with IPTables() as ipt:
            rule = {
                "chain": chain,
                "protocol": protocol,
                "src": src_ip,
                "dst": dst_ip,
                "jump": "ACCEPT"
            }
            if src_port != "any":
                rule["sports"] = [src_port]
            if dst_port != "any":
                rule["dports"] = [dst_port]

            # Check if rule already exists before adding
            existing_rules = ipt.get_rules("filter", chain)
            if any(r for r in existing_rules if r.get("src") == src_ip and r.get("dst") == dst_ip):
                logging.info(f"Skipping duplicate rule: {rule}")
                return

            ipt.append_rule("filter", rule)
            logging.info(f"Applied rule: {rule}")

    except Exception as e:
        logging.error(f"Failed to apply rule: {rule}, Error: {e}")


def generate_iptables_rules_host_level(ip: str, df_flows: pd.DataFrame):
    """
    Generates and applies iptables rules at the host level.
    Allows inbound/outbound communication for all hosts in the segmentation.
    """
    host_level = host_level_segmentation(ip, df_flows)

    # for each communication partner/host, accept in- and outbound communication with this host
    for _, row in host_level.iterrows():
        apply_rule("INPUT", "all", row["ip"], ip, "any", "any")
        apply_rule("OUTPUT", "all", ip, row["ip"], "any", "any")


def generate_iptables_rules_application_level(ip: str, df_flows: pd.DataFrame):
    """
    Generates and applies iptables rules at the application level.
    Handles uni-directional and bi-directional communication based on protocol and ports.
    """
    app_level = application_level_segmentation(ip, df_flows)

    # corner cases:
    #   - uni-directional communication: allows only this specific flow from src to dst
    #   - bi-directional communication: allows communication for host, protocol, and application port in both directions
    #   - is given IP the src or dst in streams? (-> affects required chain: INPUT or OUTPUT)
    for _, row in app_level.iterrows():
        protocol = "tcp" if row["protocol"] == 6 else "udp" if row["protocol"] == 17 else "all"
        src_ip = row["src_ip"]
        dst_ip = row["dst_ip"]
        src_port = str(int(row["src_port"])) if pd.notna(row["src_port"]) else "any"
        dst_port = str(int(row["dst_port"])) if pd.notna(row["dst_port"]) else "any"

        # Determine if the IP is the source or destination
        if ip == dst_ip:
            chain = "INPUT"
        elif ip == src_ip:
            chain = "OUTPUT"
        else:
            continue

        if row["bi-directional"]:
            apply_rule("INPUT", protocol, src_ip, dst_ip, src_port, dst_port)
            apply_rule("OUTPUT", protocol, dst_ip, src_ip, dst_port, src_port)
        else:
            apply_rule(chain, protocol, src_ip, dst_ip, src_port, dst_port)