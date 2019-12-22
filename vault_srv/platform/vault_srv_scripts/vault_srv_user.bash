#!/usr/bin/env bash

# ---------------------------------------------------------------------------
#   File        : vault_srv_user.bash
#   Description : users for Vault Server
#   Author      : Eric Siegel
#
# Copyright © 2019, GNU Public License
# ---------------------------------------------------------------------------

echo "####################################################################"
echo "STARTING vault_srv_user.bash"
echo "####################################################################"


# Add Group cs
groupadd -f -g 850 -r cs


# Add login Users
useradd -c "CS Admin" -e 2040-01-01 -f -1 -g cs -m -N -u 860 -p '$6$6uly.okBgcjg9id1$qthP75KlcWBEJFGOM1/T.4PrVGzL5ICHSnrYBBuFEVZNQmg0xaWgtg7mnYY0EyVWfUyqpwa8iyfOvBq2DKctM/' csAdmin
useradd -c "CS Backup" -e 2040-01-01 -f -1 -g cs -m -N -u 865 -p '$6$6uly.okBgcjg9id1$qthP75KlcWBEJFGOM1/T.4PrVGzL5ICHSnrYBBuFEVZNQmg0xaWgtg7mnYY0EyVWfUyqpwa8iyfOvBq2DKctM/' csBackup

# Add Service account
useradd -u 881 -c "CS Service User" -g cs -r csService

# Set Shell
usermod --shell /bin/bash csAdmin
usermod --shell /bin/bash csBackup
usermod --shell /bin/bash csService

# Load to Sudo Group
adduser csAdmin sudo
