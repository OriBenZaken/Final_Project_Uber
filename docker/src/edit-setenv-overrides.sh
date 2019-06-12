#!/bin/bash
cd /usr/local/i9e/gigaspaces-insightedge-enterprise-14.5.0-m7/bin/
MACHINE_IP=$(curl https://ipinfo.io/ip)
echo "export XAP_PUBLIC_HOST=$MACHINE_IP" | sudo tee setenv-overrides.sh


