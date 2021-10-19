#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ************************************************************
#
#     osctest.py
#
#     Copyright 2021 Yabe.Kazuhiro
#
# ************************************************************

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys
import argparse
import fileinput
from logging import getLogger, StreamHandler, DEBUG, WARNING, INFO
from pythonosc import udp_client
from pythonosc import osc_server
from pythonosc import dispatcher

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)

def rx_filter(address, args):
    print(address, args)

def example1(addr, port, rx_port):
    dispatch = dispatcher.Dispatcher()
    dispatch.map('*', rx_filter)
    server = osc_server.BlockingOSCUDPServer((addr, rx_port), dispatch)

    client = udp_client.SimpleUDPClient(addr, port)
    client.send_message('/motor', [1, 100, -100, 500])

def options(argv):
    op = argparse.ArgumentParser()
    op.add_argument('--dry-run', action='store_true', help='do not perform actions')
    op.add_argument('-v', '--verbose', action='store_true', help='verbose mode')
    op.add_argument('-q', '--quiet', action='store_true', help='quiet mode')
    op.add_argument('-a', '--address', action='store', default='localhost', help='OSC server address')
    op.add_argument('-p', '--port', action='store', default=3334, help='OSC server port (TX)')
    op.add_argument('-r', '--rx-port', action='store', default=3333, help='OSC server port (RX)')
    op.add_argument('argv', nargs='*', help='args')
    opt = op.parse_args(argv[1:])
    # set logging level
    if opt.quiet:
        loglevel = WARNING
    elif opt.verbose:
        loglevel = DEBUG
    else:
        loglevel = INFO
    handler.setLevel(loglevel)
    logger.setLevel(loglevel)
    return opt


def main(argv):
    opt = options(argv)

    if len(argv) >= 1:
        example1(opt.address, opt.port, opt.rx_port)
    else:
        pass

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))

