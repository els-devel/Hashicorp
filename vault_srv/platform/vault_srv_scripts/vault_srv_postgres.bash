#!/usr/bin/env bash

# ---------------------------------------------------------------------------
#   File        : vault_srv_postgres.bash
#   Description : configs for postgresql12
#   Author      : Eric Siegel
#
# Copyright © 2019, GNU Public License
# ---------------------------------------------------------------------------

CONF_DIR='./postgresql_config'
PG_CONF_DIR='/etc/postgresql/12/main'

cp $CONF_DIR/pg_hba.conf $PG_CONF_DIR/pg_hba.conf
chown postgres.postgres $PG_CONF_DIR/pg_hba.conf
chmod 0640 $PG_CONF_DIR/pg_hba.conf

cp $CONF_DIR/postgresql.conf $PG_CONF_DIR/postgresql.conf
chown postgres.postgres $PG_CONF_DIR/postgresql.conf
chmod 0644 $PG_CONF_DIR/postgresql.conf



systemctl restart postgresql.service
