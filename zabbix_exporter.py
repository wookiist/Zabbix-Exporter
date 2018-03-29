#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time

from args_parser import args_parser
import os
from prometheus_client import start_http_server, Summary, Metric
from prometheus_client.core import GaugeMetricFamily, REGISTRY
from prometheus_client.parser import text_string_to_metric_families
from pyzabbix import ZabbixAPI

DEBUG = int(os.environ.get('DEBUG', '0'))


class ZabbixCollector(object):
    def __init__(self, url, username, password):
        self._url = url.rstrip("/")
        #self._username = username
        #self._password = password
        self._zapi = ZabbixAPI(self._url + '/zabbix')
        self._zapi.login(username, password)

    def collect(self):
        # define environment variables
        start = time.time()


        # Request data from Zabbix
        #jobs = self._request_data()

        # create a prometheus metric
        metric = Metric('zabbix_warning', 'Current Zabbix Warning Count', 'gauge')
        # Get a list of all issues (AKA tripped triggers)

        triggers = self._zapi.trigger.get(only_true=1,
                                    skipDependent=1,
                                    monitored=1,
                                    active=1,
                                    output='extend',
                                    expandDescription=1,
                                    selectHosts=['host'],
                                    )

        # Do another query to find out which issues are Unacknowledged
        unack_triggers = self._zapi.trigger.get(only_true=1,
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

    def _request_data(self):
        # Request exactly the information we need from Jenkins
        pass

    def _setup_empty_prometheus_metrics(self):
        # The metrics we want to export
        #self._prometheus_metrics = {}
        pass


def main():
    try:
        args = args_parser()
        port = int(args.port)

        # start the webserver on the required port
        start_http_server(9288)
        REGISTRY.register(ZabbixCollector(args.url, args.username, args.password))
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(" Keyboard Interrupted")
        exit(0)


if __name__ == "__main__":
    main()