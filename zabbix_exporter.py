#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
import os
from prometheus_client import start_http_server, Metric
from prometheus_client.core import REGISTRY
from pyzabbix import ZabbixAPI

DEBUG = int(os.environ.get('DEBUG', '0'))


class ZabbixCollector(object):
    def __init__(self):
        pass

    def collect(self):
        # define environment variables
        zabbix_exp_url = os.environ.get('ZABBIX_EXP_URL', 'http://localhost/')
        zabbix_exp_username = os.environ.get('ZABBIX_EXP_USERNAME', 'Admin')
        zabbix_exp_password = os.environ.get('ZABBIX_EXP_PASSWORD', 'zabbix')

        zapi = ZabbixAPI(zabbix_exp_url)
        zapi.login(zabbix_exp_username, zabbix_exp_password)

        # create a prometheus metric
        metric = Metric('zabbix_warning', 'Current Zabbix Warning Count', 'gauge')
        # Get a list of all issues (AKA tripped triggers)

        triggers = zapi.trigger.get(only_true=1,
                                    skipDependent=1,
                                    monitored=1,
                                    active=1,
                                    output='extend',
                                    expandDescription=1,
                                    selectHosts=['host'],
                                    )

        # Do another query to find out which issues are Unacknowledged
        unack_triggers = zapi.trigger.get(only_true=1,
                                          skipDependent=1,
                                          monitored=1,
                                          active=1,
                                          output='extend',
                                          expandDescription=1,
                                          selectHosts=['host'],
                                          withLastEventUnacknowledged=1,
                                          )

        unack_trigger_ids = [t['triggerid'] for t in unack_triggers]

        for t in triggers:
            t['unacknowledged'] = True if t['triggerid'] in unack_trigger_ids \
                else False

        # Print a list containing only "tripped" triggers
        # Sum triggers which value is 1
        warn_cnt = 0
        for t in triggers:
            if int(t['value']) == 1:
                warn_cnt += 1

        # append data to the metric
        metric.add_sample('zabbix_warning', value=int(warn_cnt), labels={})
        yield metric


def main():
    try:
        # start the webserver on the required port
        start_http_server(9288)
        REGISTRY.register(ZabbixCollector())
    except KeyboardInterrupt:
        print(" Keyboard Interrupted")
        exit(0)


if __name__ == "__main__":
    main()
