#!/usr/bin/env bash

# ---------------------------------------------------------------------------
#   File        : vault_srv_firewall.bash
#   Description : Setup fire wall for vault server
#   Author      : Eric Siegel
#
# Copyright © 2019, GNU Public License
# ---------------------------------------------------------------------------

VAULT_SRV_IP=

echo "####################################################################"
echo "STARTING vault_srv_firewall.bash"
echo "####################################################################"

ufw enable
# Local host
ufw allow from 127.0.0.1/32 to 127.0.0.1 port 5432 proto tcp
# VPN
ufw allow from 10.16.128.0/24 to $VAULT_SRV_IP port 5432 proto tcp

ufw allow http
ufw allow https
ufw allow ssh
ufw allow 8200

systemctl restart ufw

