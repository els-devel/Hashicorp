#!/usr/bin/env bash

# ---------------------------------------------------------------------------
#   File        : vault_srv_install.bash
#   Description : Setup for Vault Server
#   Author      : Eric Siegel
#
# Copyright © 2019, GNU Public License
# ---------------------------------------------------------------------------

SCRIPT_DIR='./vault_srv_scripts'


echo "####################################################################"
echo "STARTING vault_srv_install.bash"
echo "####################################################################"

# ### vault-srv Users 
$SCRIPT_DIR/vault_srv_user.bash

# ### repo script
$SCRIPT_DIR/vault_srv_repo.bash

# ### apt script
$SCRIPT_DIR/vault_srv_apt.bash

# ### pip install script
$SCRIPT_DIR/vault_srv_pip.bash

# ### firewall script
$SCRIPT_DIR/vault_srv_firewall.bash

# ### postgresql setup
$SCRIPT_DIR/vault_srv_postgres.bash

