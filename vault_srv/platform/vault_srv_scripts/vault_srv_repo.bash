#!/usr/bin/env bash

# ---------------------------------------------------------------------------
#   File        : vault_srv_repo.bash
#   Description : APT repo installs
#   Author      : Eric Siegel
#
# Copyright © 2019, GNU Public License
# ---------------------------------------------------------------------------

# Assumes 19.10

# Get a few packages to start
apt install wget curl vim


# PostgreSQL 12
wget -q -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" | tee /etc/apt/sources.list.d/pgdg.list

apt update
