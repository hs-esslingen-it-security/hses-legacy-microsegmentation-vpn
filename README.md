# Security Gateway for Automated Micro-Segmentation and VPN Encryption in Industrial Legacy Systems

This repository contains the accompanying code and data for the Proof-of-Concept (PoC) of the paper on securely integrating legacy devices into industrial networks. The goal is to automate and implement micro-segmentation and VPN encryption for legacy devices through security gateways.

## Repository Structure
The repository is structured as follows:

- **`traffic_captures/`** - Contains pre-processed traffic captures from the SWaT testbed along with the scripts used for pre-processing.
- **`demo/`** - Includes a Jupyter Notebook demonstrating the key steps: communication relations analysis (+ visualization), micro-segmentation via firewall rule generation, and VPN configuration.
- **`scripts/`** - contains the core scripts:
  - `flow_analysis.py` - Analyzes communication relations.
  - `visualize_relations.py` - Visualizes communication relations.
  - `micro_segmentation.py` - Aggregates suitable micro-segments.
  - `firewall_rules_generation.py` - Generates firewall rules to enforce the microsegments.
  - `wireguard.py` - Configures VPN settings.
- **`PoC/`** - Contains the PoC, i.e., a zipped Docker network implementing the described steps, providing a reproducible setup.



## To-Do
- [ ] Upload Scripts
- [ ] Upload Demo
- [ ] Upload PoC/Docker network


## Usage
After cloning the repository, navigate to the relevant directories:

- Run the Jupyter Notebook in `demo/` to explore the PoC logic.
- Use the scripts in `scripts/` for in-depth analysis and configuration.
- Deploy the provided Docker network to replicate the testbed environment.
