import pandas as pd
import logging
from micro_segmentation import *
import subprocess

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

########################
# firewall rule handling
########################

def apply_rule(chain: str, protocol: str, src_ip: str, dst_ip: str, src_port: str, dst_port: str):
    """
    Apply an iptables rule.
    
    :param chain: The chain to apply the rule to (e.g., "INPUT", "OUTPUT", "FORWARD").
    :param protocol: The protocol to match (e.g., "tcp", "udp").
    :param src_ip: Source IP address.
    :param dst_ip: Destination IP address.
    :param src_port: Source port.
    :param dst_port: Destination port.
    """
    # base command
    command = ["sudo", "iptables", "-A", chain, "-p", protocol, "-s", src_ip, "-d", dst_ip]
    # port option only if specific protocol is given
    if protocol != "all":
        if src_port != "any":
            command += ["--sport", src_port]
        if dst_port != "any":
            command += ["--dport", dst_port]
    command += ["-j", "ACCEPT"]
    
    try:
        subprocess.run(command, check=True)
        print("Rule applied successfully:", " ".join(command))
    except subprocess.CalledProcessError as e:
        print("Error applying rule:", e)


# add logging (?): iptables -A OUTPUT -j LOG --log-prefix "Dropped packet: " --log-level 4
# Drop at the end: iptables -A INPUT -j DROP
def log_and_drop(chain: str):
    """
    Apply (a LOG rule followed by) a DROP rule at the end of the given chain.

    :param chain: The chain to apply the rule to (e.g., "INPUT", "OUTPUT", "FORWARD").
    """
    # base command
    base_command = ["sudo", "iptables", "-A", chain]
    
    # Add the log action
    # log_command = base_command + ["-j", "LOG", "--log-prefix", '"Dropped packet: "', "--log-level", "4"]
    # try:
    #     subprocess.run(log_command, check=True)
    #     print("LOG rule applied successfully:", " ".join(log_command))
    # except subprocess.CalledProcessError as e:
    #     print("Error applying LOG rule:", e)

    # Add the drop action
    drop_command = base_command + ["-j", "DROP"]
    try:
        subprocess.run(drop_command, check=True)
        print("DROP rule applied successfully:", " ".join(drop_command))
    except subprocess.CalledProcessError as e:
        print("Error applying DROP rule:", e)




def generate_firewall_rules_host_level(ip: str, df_flows: pd.DataFrame):
    """
    Generates and applies firewall rules at the host level.
    Allows inbound/outbound communication for all hosts in the segmentation.
    """
    host_level = host_level_segmentation(ip, df_flows)

    # for each communication partner/host, accept in- and outbound communication with this host
    logging.info(f"Generate firewall rules for {ip}")
    for _, row in host_level.iterrows():
        apply_rule("INPUT", "all", row["ip"], ip, "any", "any")
        apply_rule("OUTPUT", "all", ip, row["ip"], "any", "any")

    log_and_drop("INPUT")
    log_and_drop("OUTPUT")


def generate_firewall_rules_application_level(ip: str, df_flows: pd.DataFrame):
    """
    Generates and applies firewall rules at the application level.
    Handles uni-directional and bi-directional communication based on protocol and ports.
    """
    app_level = application_level_segmentation(ip, df_flows)

    # corner cases:
    #   - uni-directional communication: allows only this specific flow from src to dst
    #   - bi-directional communication: allows communication for host, protocol, and application port in both directions
    #   - is given IP the src or dst in streams? (-> affects required chain: INPUT or OUTPUT)
    logging.info(f"Generate firewall rules for {ip}")
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

    log_and_drop("INPUT")
    log_and_drop("OUTPUT")


