import argparse
import pandas as pd
from micro_segmentation import *
from firewall_rules_generation import *

def main():
    # Set up argument parser for command-line inputs
    parser = argparse.ArgumentParser(description="Micro-segmentation and firewall rules generation")
    parser.add_argument("csv", type=str, help="Path to the flows CSV file")
    parser.add_argument("ip", type=str, help="IP address to analyze")
    parser.add_argument("granularity", choices=["device", "application"], help="Granularity level: device or application")
    
    args = parser.parse_args()

    # Process pcap and extract network flows into pandas DataFrame
    df_flows = pd.read_csv(args.csv, sep=',')
    if args.granularity == "device":
        # Perform host-level segmentation
        generate_firewall_rules_host_level(args.ip, df_flows)
    else:
        # Perform application-level segmentation 
        generate_firewall_rules_application_level(args.ip, df_flows)

if __name__ == "__main__":
    main()