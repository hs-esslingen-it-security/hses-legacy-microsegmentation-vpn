
import subprocess
import logging
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

gw_to_ip_map = {"esp-gw1": "192.168.1.10",
                "esp-gw2": "192.168.1.20",
                "esp-gw3": "192.168.1.30",
                "esp-gw4": "192.168.1.40",
                "esp-gw5": "192.168.1.50",
                "esp-gw6": "192.168.1.60",
                "scada":   "192.168.1.100"}

def send(filename: str = "demo.pcap", container: str = "esp-gw6", count: int = 1000):
    #subprocess.run(f"docker exec {container} ls".split(" "), check=True)
    #subprocess.run(f"docker exec {container} /scripts/replay.sh".split(" "), check=True)
    subprocess.run(f"docker exec {container} /scripts/replay.sh {filename} {gw_to_ip_map[container]}".split(" "), check=True)


def main():
    FILENAME = "unauthorized-gw.pcap"
    send(filename=FILENAME)

if __name__ == "__main__":
    main()