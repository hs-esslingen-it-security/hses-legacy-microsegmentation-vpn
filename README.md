# Security Gateway for Automated Micro-Segmentation and VPN Encryption in Industrial Legacy Systems 

This repository contains the accompanying code and data for the **Proof-of-Concept (PoC)** of the paper "Security Gateway for Automated Micro-Segmentation and VPN Encryption in Industrial Legacy Systems", on securely integrating legacy devices into industrial networks. The goal is to automate and implement micro-segmentation and VPN encryption for legacy devices through security gateways, thereby ensuring a seamless migration towards a more secure infrastructure. 

## Repository Structure
The repository is structured as follows:

- 📁 **`PoC/`** - Contains a Docker network implementing the described steps, providing a reproducible setup.

- 📁 **`data/`** - Contains pre-processed traffic captures from the testbed (topology displayed), the results of the flow analysis, and the traffic captures used in the PoC to test unauthorized access.
- 📁 **`scripts/`** - contains the core scripts:
  - `flow_analysis.py` - Analyzes communication relations.
  - `visualize_relations.py` - Visualizes communication relations.
  - `micro_segmentation.py` - Aggregates devices into micro-segments based on identified relations.
  - `firewall_rules_generation.py` - Generates firewall rules for micro-segmentation.
  - `wireguard.py` - Generates VPN configurations.
  - We also include a 📓 `notebook.ipynb` demonstrating the key steps: communication relations analysis (+ visualization), micro-segmentation via firewall rule generation, and VPN configurations generation.

## Setup & Usage
After cloning the repository, navigate to the relevant directories:

1. Navigate to 📁 `PoC/`
1. Deploy the provided Docker network with `docker compose up`.
    1. This step starts six PLCs and a SCADA system, each sending traffic from a real testbed.
    1. You can modify the replayed traffic with the pcap stored in 📁 `PoC/shared-volume/shared-pcaps/`
1. Navigate to 📁 `PoC/automation`
1. Install the required Python dependencies with `pip install -r requirements.txt`
1. Execute the attack with `python 01_attack.py` and see that it is successful
1. Deploy the segmentation with `python 00_segmentation.py`
1. Execute the attack again with `python 01_attack.py` and see that it is unsuccessful