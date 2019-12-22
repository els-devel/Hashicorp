#!/usr/bin/env python3

import subprocess
import sys
import requests
import zipfile
import pexpect
import syslog


def run(cmd):
    try:
        subprocess.run(cmd, shell=True)
    except Exception as e:
        syslog.LOG_ERR(f"Encounted exception on command {cmd}, error: {e}")


config = """storage "postgresql" {
 connection_url = "postgres://csvault:1$Password!@localhost:5432/vault"
}

listener "tcp" {
 address     = "localhost:8200"
 tls_disable = 1
}

api_addr = "localhost:8200"
"""


class Vault(object):

    def __init__(self):
        self.policy = None
        self.vault_path = "/vault"
        self.vault_ip = "10.0.0.0"
        self.postgres_meta = {"table_name": "vault_secrets"}
        self.token = None
        self.postgres_user = "postgres"
        self.postgres_password = "1$Password"
        self.postgres_db = "my-postgres-database"
        with open(self.vault_path + "/config.hcl") as file:
            file.write(config)
        self.key1 = self.key2 = self.key3 = None
        self.key_server_ips = {
            "servers": {
                1: "10.0.0.0",
                2: "10.0.0.0",
                3: "10.0.0.0",
                4: "10.0.0.0",
                5: "10.0.0.0"
            }}
        self.key_server_users = {
            "servers": {
                1: "user1",
                2: "user2",
                3: "user3",
                4: "user4",
                5: "user5"
            }}

    @staticmethod
    def _request_get(url, stream=False):
        try:
            if stream:
                r = requests.get(url, stream=True, timeout=180)
            r = requests.get(url, timeout=180)
        except requests.exceptions.ReadTimeout:
            syslog.LOG_ERR("REQUEST TIMED OUT")
            sys.exit(1)
        syslog.LOG_INFO(f"Request response with status code: {r.status_code}")
        if r.ok:
            return r
        raise requests.exceptions.HTTPError

    def _vault_install(self):
        vault_zip = self._request_get("https://releases.hashicorp.com/vault/$VERSION/vault_$VERSION_linux_amd64.zip",
                                      stream=True)
        with zipfile.ZipFile(vault_zip) as vault:
            vault.extractall(path=self.vault_path)

    def _vault_init(self, unseal=False):
        run("vault server -config=config.hcl ")
        if unseal:
            key_output = subprocess.check_output("vault operator init")
        key_output = subprocess.check_output("vault operator init")

    def _get_keys(self):
        # ssh self.key_server_user@self.key_server_ip
        # self.key1, self.key2, self.key3
        pass

    def unseal(self):
        proc = pexpect.spawn("vault operator unseal")
        keys = [self.key1, self.key2, self.key3]
        for key in keys:
            proc.expect("")
            proc.send(key)
        proc.interact()

    def api_unseal(self):
        keys = [self.key1, self.key2, self.key3]
        for key in keys:
            requests.post(url=self.vault_ip, data='{"key": %s }' % key)

    def _make_postgres_tables(self):
        sql_statements = [
            f'CREATE TABLE {self.postgres_meta["table_name"]} '
            '(parent_path TEXT COLLATE "C" NOT NULL, path TEXT COLLATE "C", key TEXT COLLATE "C", '
            'value BYTEA, CONSTRAINT pk PRIMARY KEY (path, key));',
            f'CREATE INDEX parent_path_idx ON {self.postgres_meta["table_name"]} (parent_path);'
        ]
        for statement in sql_statements:
            run(f"su postgres -c psql {statement}")

    def postgres_config(self):
        self._make_postgres_tables()
        run("vault secrets enable database")
        run('vault write database/config/my-postgresql-database plugin_name=postgresql-database-plugin'
            'allowed_roles="my-role" connection_url="postgresql://{{username}}:{{password}}@localhost:5432/" '
            f'username="{self.postgres_user}" password={self.postgres_password}')
        run("""vault write database/roles/my-role db_name=%s 
        creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; 
        GRANT SELECT ON ALL TABLES IN SCHEMA public TO \"{{name}}\";" default_ttl="1h" max_ttl="24h" """ % self.postgres_db)
        self.token = subprocess.check_output("echo $(vault token create) | grep token | "
                                             "awk {'print $1'}", shell=True, text=True)

    def _get_value(self, key, table):
        self.username = subprocess.check_output("echo $(vault read database/creds/my-role) | grep username | "
                                                "awk {'print $1'}", shell=True, text=True)
        self.password = subprocess.check_output("echo $(vault read database/creds/my-role) | grep password | "
                                                "awk {'print $1'}", shell=True, text=True)
        cmd = f"SELECT {key} FROM TABLE {table};"
        key = subprocess.check_output(f"psql --username {self.username} --dbname vault -c {cmd}", shell=True, text=True)
        return key
