# Security Gateway for Automated Micro-Segmentation and VPN Encryption in Industrial Legacy Systems 

This repository contains the accompanying code and data for the **Proof-of-Concept (PoC)** of the paper "Security Gateway for Automated Micro-Segmentation and VPN Encryption in Industrial Legacy Systems", on securely integrating legacy devices into industrial networks. The goal is to automate and implement micro-segmentation and VPN encryption for legacy devices through security gateways, thereby ensuring a seamless migration towards a more secure infrastructure. 

## Repository Structure
The repository is structured as follows:

- 📁 **`data/`** - Contains pre-processed traffic captures from the SWaT testbed [1] (topology displayed), the results of the flow analysis, and the traffic captures used in the PoC to test unauthorized access.
- 📁 **`scripts/`** - contains the core scripts:
  - `flow_analysis.py` - Analyzes communication relations.
  - `visualize_relations.py` - Visualizes communication relations.
  - `micro_segmentation.py` - Aggregates devices into micro-segments based on identified relations.
  - `firewall_rules_generation.py` - Generates firewall rules for micro-segmentation.
  - `wireguard.py` - Generates VPN configurations.
  - We also include a 📓 `notebook.ipynb` demonstrating the key steps: communication relations analysis (+ visualization), micro-segmentation via firewall rule generation, and VPN configurations generation.
- 📁 **`PoC/`** - Contains a Docker network implementing the described steps, providing a reproducible setup.


## Setup & Usage
After cloning the repository, navigate to the relevant directories:

- Run the 📓 `notebook.ipynb` to explore the PoC logic.
- Deploy the provided Docker network to replicate the 📁 `PoC/`.


## Upcoming improvements:
- [ ] Update scripts (wireguard)


[1]: A. P. Mathur and N. O. Tippenhauer, "SWaT: a water treatment testbed for research and training on ICS security," 2016 International Workshop on Cyber-physical Systems for Smart Water Networks (CySWater), Vienna, Austria, 2016, pp. 31-36, doi: 10.1109/CySWater.2016.7469060.