#!/usr/bin/env bash

# ---------------------------------------------------------------------------
#   File        : vault_srv_pip.bash
#   Description : pip installs
#   Author      : Eric Siegel
#
# Copyright © 2019, GNU Public License
# ---------------------------------------------------------------------------


pip_list="
pep8
Cython
xmltodict
psycopg2-binary
dpath
dateparser
"
python3 -m pip install --upgrade pip

for p in $pip_list; do
	python3 -m pip install $p
done
