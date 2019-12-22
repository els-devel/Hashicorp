#!/usr/bin/env bash

# ---------------------------------------------------------------------------
#   File        : vault_srv_apt.bash
#   Description : APT install for Vault Server
#   Author      : Eric Siegel
#
# Copyright © 2019, GNU Public License
# ---------------------------------------------------------------------------

apt update

BASE="
vim
wget
curl
ca-certificates
google-chrome-stable
zsh
openssl
openvpn
tree
locate
"

PACKAGE="
linux-headers-$(uname -r)
build-essential
git
gitk
meld
python3
python3-pip
apache2
memcached
libmemcached-tools
nodejs
npm
yui-compressor
sassc
python3
python3-virtualenv
python3-pip
"

POSTGRESQL="
postgresql-12
"

apt install $BASE $PACKAGE $POSTGRESQL
