# Security Gateway for Automated Micro-Segmentation and VPN Encryption in Industrial Legacy Systems

This repository contains the accompanying code and data for the Proof-of-Concept (PoC) of the paper on securely integrating legacy devices into industrial networks. The goal is to automate and implement micro-segmentation and VPN encryption for legacy devices through security gateways.

## Repository Structure
The repository is structured as follows:

- **`data/`** - Contains pre-processed traffic captures from the SWaT testbed along with the scripts used for pre-processing.
- **`scripts/`** - contains the core scripts:
  - `flow_analysis.py` - Analyzes communication relations.
  - `visualize_relations.py` - Visualizes communication relations.
  - `micro_segmentation.py` - Aggregates suitable micro-segments.
  - `firewall_rules_generation.py` - Generates firewall rules to enforce the microsegments.
  - `wireguard.py` - Configures VPN settings.
  
  It also includes a **Jupyter Notebook** demonstrating the key steps: communication relations analysis (+ visualization), micro-segmentation via firewall rule generation, and VPN configuration.
- **`PoC/`** - Contains the PoC, including a zipped Docker network implementing the described steps, providing a reproducible setup.


## To-Do
- [ ] Upload scripts
- [ ] Extend demo/notebook
- [ ] Upload PoC/docker network


## Usage
After cloning the repository, navigate to the relevant directories:

- Run the Jupyter Notebook to explore the PoC logic.
- Deploy the provided Docker network to replicate the testbed environment.
