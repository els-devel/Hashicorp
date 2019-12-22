#!/usr/bin/env bash

# ---------------------------------------------------------------------------
#   File        : vault_srv_curk.bash
#   Description : curl install for Vault Server
#   Author      : Eric Siegel
#
# Copyright © 2019, GNU Public License
# ---------------------------------------------------------------------------

VERSION=1.3.0
VAULT_IP=10.16.0.0

curl -o /vault/bin/vault.zip https://releases.hashicorp.com/vault/$VERSION/vault_$VERSION_linux_amd64.zip
cd /vault/bin/vault.zip
unzip vault.zip

echo "PATH=/vault/bin" >> /etc/environment.d/vault.conf
echo "
#!/bin/bash
export VAULT_ADDR='http://${VAULT_IP}:8200'
" >> /etc/profile.d/vault.sh
chmod +x /etc/profile.d/vault.sh

systemctl daemon-reload
systemctl start vault