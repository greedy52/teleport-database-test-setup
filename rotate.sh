#!/bin/bash

type="db"
if [[ -n "$1" ]]; then 
    type="$1"
fi

echo "=== Rotation for ${type}"

for phase in "init" "update_clients" "update_servers" "standby"
do
    echo "Rotating phase ${phase}"
    tctl auth rotate --phase=${phase} --type=${type} --manual
    sleep 5
    tctl status
done
