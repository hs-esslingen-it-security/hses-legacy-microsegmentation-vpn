#!/bin/bash
echo $1;

IFS=',' read -r -a tunnels <<< "$1"
for element in "${tunnels[@]}"
do
    echo "$element"
    IFS='__' read -r -a config <<< "$element"
    echo "${config[@]}"
    echo "${config[0]}: ${config[8]}"
    echo "${config[2]}: ${config[10]}"
    echo "${config[4]} - ${config[6]}"
    echo "${config[8]} - ${config[10]}"

    docker exec ${config[0]} ip link add dev wg${config[4]}${config[6]} type wireguard
    docker exec ${config[0]} ip address add dev wg${config[4]}${config[6]} 192.168.1${config[4]}${config[6]}.${config[4]}/24
    docker exec ${config[0]} ip address add dev wg${config[4]}${config[6]} 192.168.1${config[4]}${config[6]}.${config[4]} peer 192.168.1.${config[6]}0
    docker exec ${config[0]} wg set wg${config[4]}${config[6]} listen-port 518${config[4]}${config[6]} private-key /data/wg_private.key peer ${config[10]} allowed-ips 0.0.0.0/0 endpoint 192.168.1.10${config[6]}:518${config[6]}${config[4]} persistent-keepalive 25
    docker exec ${config[0]} ip link set dev wg${config[4]}${config[6]} up

    docker exec ${config[2]} ip link add dev wg${config[4]}${config[6]} type wireguard
    docker exec ${config[2]} ip address add dev wg${config[4]}${config[6]} 192.168.1${config[4]}${config[6]}.${config[6]}/24
    docker exec ${config[2]} ip address add dev wg${config[4]}${config[6]} 192.168.1${config[4]}${config[6]}.${config[6]} peer 192.168.1.${config[4]}0
    docker exec ${config[2]} wg set wg${config[4]}${config[6]} listen-port 518${config[6]}${config[4]} private-key /data/wg_private.key peer ${config[8]} allowed-ips 0.0.0.0/0 endpoint 192.168.1.10${config[4]}:518${config[4]}${config[4]} persistent-keepalive 25
    docker exec ${config[2]} ip link set dev wg${config[4]}${config[6]} up

done

