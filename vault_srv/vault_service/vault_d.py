#! python3
# -*- coding: utf-8 -*-

# ---------------------------------------------------------------------------
#   File        : flow_helper.py
#   Description : Flow Helper Main File
#
# Copyright © 2019, Centered Solutions - All Rights Reserved
# Proprietary and confidential
# ---------------------------------------------------------------------------

# Imports
import subprocess
import signal
import argparse
import sys
import logging
import logging.config
from logging.handlers import SysLogHandler
from multiprocessing import Event
from multiprocessing import freeze_support

__copyright__ = "Copyright © 2019, Centered Solutions"
__author__ = "Brian Broussard"
__email__ = "brian@centeredsolutions.com"

PG_NAME = "Vault"

# ##########################################
# Args
# ##########################################
parser = argparse.ArgumentParser(description='fEncrypt')

parser.add_argument(
    '--logger', '-l',
    dest='logger',
    default='logger_normal',
    metavar='logger',
    choices=['logger_normal', 'logger_screen'],
    help='Logger type.'
)

parser.add_argument(
    '--log_level', '-m',
    dest='log_level',
    default='INFO',
    metavar='log_level',
    choices=['INFO', 'DEBUG'],
    help='Log Level.'
)

args = parser.parse_args()

# ##########################################
# Logs
# ##########################################
LOG_CONFIG = None
LOG_CONFIG_NORMAL = {
    'disable_existing_loggers': False,
    'version': 1,
    'formatters': {
        'formatter_syslog': {
            'format': "flow_encrypt [%(filename)s:%(lineno)s] %(message)s",
        },
    },
    'handlers': {
        'handler_syslog': {
            'class': 'logging.handlers.SysLogHandler',
            'address': '/dev/log',
            'facility': SysLogHandler.LOG_SYSLOG,
            'formatter': 'formatter_syslog'
        },
    },
    'loggers': {
        '': {
            'handlers': ['handler_syslog'],
        },
    }
}

LOG_CONFIG_SCREEN = {
    'disable_existing_loggers': False,
    'version': 1,
    'formatters': {
        'formatter_stdout': {
            'format': '%(filename)-20s line:%(lineno)-4d %(levelname)-8s %(message)s',
        },
    },
    'handlers': {
        'handler_stdout': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'formatter_stdout'
        },
    },
    'loggers': {
        '': {
            'handlers': ['handler_stdout'],
        }
    }
}


def init_logging(_name=__name__, logger_type='logger_normal', pg_name=None, log_level=None):
    logging.config.dictConfig(get_logging_dict_config(logger_type, pg_name))
    log = logging.getLogger()
    log.setLevel(log_level)
    pg_start(log, pg_name)
    return log


def get_logging_dict_config(logger_type='logger_normal', pg_name=None):
    if pg_name is not None:
        LOG_CONFIG_NORMAL['formatters']['formatter_syslog'][
            'format'] = f"{pg_name} [%(filename)s:%(lineno)s] %(message)s"
    if logger_type == 'logger_screen':
        return LOG_CONFIG_SCREEN
    else:
        return LOG_CONFIG_NORMAL


def set_logger_level(logger, level):
    if level in ['DEBUG', 'INFO', 'WARNING', 'ERROR']:
        logger.setLevel(level)


def pg_start(logger, _name=''):
    logger.info('************************')
    logger.info('__STARTING %s', _name)
    logger.info('************************')


def pg_stop(logger, _name=''):
    logger.info('__STOPPING %s  ', _name)


args = args.parser.parse_args()
log = init_logging(_name=__name__, logger_type=args.logger, pg_name=PG_NAME, log_level=args.log_level)


def run(cmd):
    output = subprocess.run(f"{cmd}", shell=True, capture_output=True, text=True)
    if output.returncode == 0:
        log.info(f"Ran cmd: {cmd} with output: {output.stdout}")
    else:
        log.error(f"Error for cmd: {cmd} with err: {output.stderr}")
        raise OSError


class Vaultd(object):

    def __init__(self, **kwargs):
        self.stop_event = Event()
        self.name = "csVault"
        self.password = "1$Password"
        self.expiration = ""

        self.vault_init_cmds = [
            'vault server -config=/etc/vault/vault_conf.json',
            'vault audit enable file file_path=/var/log/vault_audit.log',
            'vault secrets enable database',

            'vault write database/config/my-postgresql-database \
    plugin_name=postgresql-database-plugin \
    allowed_roles="SCADA" \
    connection_url="postgresql://{{username}}:{{password}}@localhost:5432/" \
    username="csVault" \
    password="1*Password"',

            f"""vault write database/roles/SCADA \
    db_name=my-postgresql-database \
    creation_statements="CREATE ROLE \"{self.name}\" WITH LOGIN PASSWORD '{self.password}' VALID UNTIL '{self.expiration}'; \
        GRANT SELECT ON ALL TABLES IN SCHEMA public TO \"{{name}}\";" \
    default_ttl="1h" \
    max_ttl="24h" """
        ]

        self.jobs = []
        self.start()
        self._bye()

    def _bye(self):
        self.stop_event.set()
        for j in self.jobs:
            j.join()
        log.info(f"BYE {PG_NAME}")

    def sig_kill(self):
        self._bye()

    def start(self):
        try:
            signal.signal(signal.SIGHUP, self.sig_kill)
            signal.signal(signal.SIGTERM, self.sig_kill)
            signal.signal(signal.SIGPWR, self.sig_kill)
            signal.signal(signal.SIGQUIT, self.sig_kill)
        except Exception as e:
            pass

        try:
            for cmd in self.vault_init_cmds:
                run(cmd)
        except Exception as e:
            log.error("Failed to initialize vault.")
            raise e

        try:
            for j in self.jobs:
                j.start()
            signal.pause()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    freeze_support()
    v = Vaultd()
