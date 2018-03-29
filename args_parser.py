#!/usr/bin/python
# -*- coding: UTF-8 -*-

import argparse
import os


def args_parser():
    parser = argparse.ArgumentParser(
        description='zabbix exporter arguments'
    )
    parser.add_argument(
        '-p', '--port',
        metavar='port',
        required=False,
        type=int,
        help='Listen to this port',
        default=int(os.environ.get('VIRTUAL_PORT', '9288'))
    )
    parser.add_argument(
        '-u', '--url',
        metavar='url',
        required=False,
        help='Zabbix server url',
        default=os.environ.get('ZABBIX_SERVER', 'http://127.0.0.1:10051')
    )
    parser.add_argument(
        '-P', '--password',
        metavar='password',
        required=True,
        help='Zabbix api password'
    )
    parser.add_argument(
        '-U', '--username',
        metavar='username',
        required=True,
        help='Zabbix api username'
    )
    return parser.parse_args()