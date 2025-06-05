
# 📁 PoC

We provide a Docker-based network environment for evaluating micro-segmentation, firewall rules generation, and VPN configuration. The setup processes PCAP files and ensures controlled network communication among containers.

### Prerequisites
- [Docker and Docker Compose installed](https://docs.docker.com/compose/install/)
- Run with **root privileges** 


## Components
- 🖥 **Devices:** `plc1` to `plc6` with security gateways `esp-gw1` to `esp-gw6` (ESP - Edge Security Proxy), each with a configuration script (`entrypoint-plc.sh` + `entrypoint-gw.sh`), and `scada` (`entrypoint.sh`)
- 📂 **Shared Volumes:**
  - Automation of the PoC is stored in `automation/` (required Python dependencies in `requirements.txt`)
  - PCAP files are stored in `shared-volume/shared-pcaps/` (`demo.pcap` is already loaded).
- 🌐 **Networking:**
  - Gateways have fixed MAC addresses on internal interfaces for routing.
  - PLCs always communicate through their designated gateway (slight adjustments to destination MAC addresses in original SWaT .pcap).


## Usage
1. Start the environment:
 ```sh
   sudo docker compose up --build
 ```
   - This initializes the containers, where each container reads the PCAP file to forward only the packets that originate from it. To start/repeat the tcpreplay, comment in `tcpdump -r /pcaps/plc1-gw.pcap -w- 'src 192.168.1.10' | tcpreplay -ieth0 - ` in the entrypoints.
3. Execute commands/scripts on specific containers `plcx`, `esp-gwx`, or `scada`, for example:
   - Send network traffic:
 ```sh
     sudo docker exec plc2 tcpdump -r /pcaps/plc2-gw.pcap -w- 'src 192.168.1.20' | tcpreplay -ieth0 -  
 ```
   - Capture network traffic:
 ```sh
     sudo docker exec plc2 tcpdump -w /data/test.pcap -c 100
 ```
 This generates `test.pcap` in `shared-volumes/plc2/` containing 100 packets.
   - Or, **directly run a bash shell**: `sudo docker exec -it esp-gw5 bash`



### Evaluation 🚨
For evaluation, `unauthorized-gw.pcap` is included in `shared-volume/shared-pcaps/`, containing unauthorized packets from `plc6 -> plc5`. 

1. Execute the attack with `python3 01_attack.py` and see that it is successful: on `plc5` run `tcpdump -i eth0 host 192.168.1.60` to capture the unauthorized packets.
2. Deploy the segmentation `python3 00_segmentation.py --segmentation --vpn`.
3. Execute the attack again with `python3 01_attack.py` and see that it is no longer successful (no incoming packets on `plc5`).



### Special Consideration: Flow Analysis 📊
For flow analysis, we use NFStream, which has special dependencies that we could only successfully deploy for Debian Bullseye with Python 3.9. Thus, the flow analysis is handled in a separate container (`flow-eval`).

To work in this container, run 
```sh
     sudo docker exec -it flow-eval bash
```
For reproducibility and potential problems with setting up NFStream, we provide the result of the flow analysis (`flow_analysis.py` in `data/shared-scripts/`) in `demo.csv`.

`02_analyze.ipynb` provides more insights into flow analysis results, including a visualization of the network topology. 

## Test Data
The demo traffic capture used in this project is sourced from the Secure Water Treatment (SWaT) testbed [1] trace **SWaT.A6_Dec 2019** (`Dec2019_00000_20191206100500.pcap`).
We consider a simplified SWaT topology of PLC1-PLC6 and the SCADA workstation.

The traffic capture was pre-processed as follows:
- Filter traffic related to PLC1-6 and SCADA. 
- Extract the first 50,000 packets (due to file size limitations) and save them to `demo.pcap` (used in Docker network).

### PoC - Unauthorized Access Attack
The unauthorized traffic used for the evaluation in the PoC (PLC6 -> PLC5; derived from communication between PLC1 and PLC6, IP-addresses adjusted) is saved to `unauthorized.pcap`.


[1]: A. P. Mathur and N. O. Tippenhauer, "SWaT: a water treatment testbed for research and training on ICS security," 2016 International Workshop on Cyber-physical Systems for Smart Water Networks (CySWater), Vienna, Austria, 2016, pp. 31-36, doi: 10.1109/CySWater.2016.7469060.