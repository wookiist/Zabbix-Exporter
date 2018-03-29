#!/usr/bin/python

import re
import time

import os
from prometheus_client import start_http_server, Summary
from prometheus_client.core import GaugeMetricFamily, REGISTRY

DEBUG = int(os.environ.get('DEBUG', '0'))

class ZabbixCollector(object):
    def __init__(self):
        pass


def main():
    try:
        pass
    except KeyboardInterrupt:
        print(" Keyboard Interrupted")
        exit(0)


if __name__ == "__main__":
    main()