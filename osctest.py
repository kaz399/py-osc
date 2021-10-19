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
import time
import asyncio
from logging import getLogger, StreamHandler, DEBUG, WARNING, INFO
from pythonosc import udp_client
from pythonosc import osc_server
from pythonosc import dispatcher

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)

def rx_default_handler(address, *args):
    print(address, args)

dispatch = dispatcher.Dispatcher()
dispatch.set_default_handler(rx_default_handler)

async def loop(addr, port):
    client = udp_client.SimpleUDPClient(addr, port)
    for i in range(10):
        print(i)
        client.send_message('/motor', [0, 100, -100, 500])
        client.send_message('/motor', [1, 100, -100, 500])
        await asyncio.sleep(1)

async def example1(addr, port, rx_port):
    server = osc_server.AsyncIOOSCUDPServer((addr, rx_port), dispatch, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()

    await loop(addr, port)

    transport.close()
    print('done')

def options(argv):
    op = argparse.ArgumentParser()
    op.add_argument('--dry-run', action='store_true', help='do not perform actions')
    op.add_argument('-v', '--verbose', action='store_true', help='verbose mode')
    op.add_argument('-q', '--quiet', action='store_true', help='quiet mode')
    op.add_argument('-a', '--address', action='store', default='127.0.0.1', help='OSC server address')
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
        asyncio.run(example1(opt.address, opt.port, opt.rx_port))
    else:
        pass

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))

