#!/bin/sh
tcpdump -r /pcaps/$1 -w- "src $2" | tcpreplay -ieth0 -