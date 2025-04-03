import subprocess
from ipaddress import IPv4Network, IPv4Interface, IPv4Address
from typing import Dict
import logging
logger = logging.getLogger(__name__)


def generate_server_config(server_address: IPv4Interface, port: int, server_key: str, clients: Dict[IPv4Address, str]):
    server_config = f"""[Interface]
PrivateKey = {server_key}
ListenPort = {port}
Address = {server_address}
"""

    for client, client_key in clients.items():
        server_config += f"""
[Peer]
PublicKey = {client_key}
AllowedIPs = {client}
"""
    return server_config


def generate_config_for_client(server: IPv4Address, port: int, server_key: str, client_key: str,
                               client_interface: IPv4Interface):
    return f"""[Interface]
PrivateKey = {client_key}
ListenPort = {port}
Address = {client_interface.with_prefixlen}

[Peer]
PublicKey = {server_key}
Endpoint = {server}:{port}
AllowedIPs = {client_interface.network}"""


def generate_keys():
    private_key = subprocess.run('wg genkey', check=True, capture_output=True, shell=True)
    public_key = subprocess.run('wg pubkey', input=private_key.stdout, check=True, capture_output=True, shell=True)
    logger.debug(private_key)
    logger.debug(public_key)
    return {'private_key': private_key.stdout.strip().decode('utf-8'),
            'public_key': public_key.stdout.strip().decode('utf-8')}


def generate_configs(connections: int, subnet: IPv4Network, server: IPv4Address, port: int):
    configs = []
    clients = {}
    if len(list(subnet)) < connections + 3:
        logger.error('Subnet too small!')
        exit(2)
    try:
        version = subprocess.run('wg --version', check=True, capture_output=True, shell=True, text=True)
        logger.info(version.stdout.strip())
        server_keys = generate_keys()
        network_hosts = list(subnet.hosts())
        for i in range(connections):
            client_interface = IPv4Interface(f"{network_hosts[i + 1]}/{subnet.prefixlen}")
            client_keys = generate_keys()
            clients[network_hosts[i + 1]] = client_keys['public_key']
            configs.append(generate_config_for_client(server, port, server_keys['public_key'],
                                                      client_keys['private_key'],
                                                      client_interface))
        server_interface = IPv4Interface(f"{network_hosts[0]}/{subnet.prefixlen}")
        configs.insert(0, generate_server_config(server_interface, port, server_keys['private_key'], clients))
        return configs
    except subprocess.CalledProcessError:
        logger.error('Wireguard is not installed!')
        exit(1)


# if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO)
    # configs = generate_configs(1, IPv4Network('10.0.0.0/24'), IPv4Address('10.0.1.1'), 51005)

