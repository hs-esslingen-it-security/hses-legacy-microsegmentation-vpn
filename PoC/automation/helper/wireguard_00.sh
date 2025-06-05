#!/bin/bash
docker exec $1 sh -c 'wg genkey > /data/wg_private.key'
docker exec $1 sh -c 'wg pubkey < /data/wg_private.key > /data/wg_public.pub'
echo "________________$(docker exec $1 cat /data/wg_public.pub)__________________"