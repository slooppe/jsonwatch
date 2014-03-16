#!/usr/bin/env python2
# Copyright 2014 Danyil Bohdan

from __future__ import print_function

import urllib2
import argparse
import json
import sys
import subprocess
import time
import datetime
import difflib
from jsondiff import json_diff, json_flatten, json_flat_diff_invert, c_keys, json_diff_str

class json_request_url(object):
    def __init__(self, url):
        self.url = url

    def perform(self):
        return json.loads(urllib2.urlopen(self.url).read())

class json_request_command(object):
    def __init__(self, command):
        self.command = command

    def perform(self):
        return json.loads(subprocess.check_output(self.command, shell=True))

def json_print(x):
    print(json.dumps(x, indent=4))

def poll_loop(interval, req, date=False):
    prev_output = None
    output = req.perform()
    json_print(output)
    while True:
        time.sleep(interval)
        prev_output, output = output, req.perform()
        #print(prev_output, output)
        diff = json_diff(prev_output, output)
        if diff is not None:
            print(datetime.datetime.now().isoformat(), json_diff_str(diff))

def main():
    parser = argparse.ArgumentParser(description='Track changes in JSON data')
    parser.add_argument('-u', '--url', help='URL',
                        default='', required=False, metavar='url',
                        dest='url')
    parser.add_argument('-c', '--command', help='command to execute',
                        default='', required=False, metavar='command',
                        dest='command')
    parser.add_argument('-n', '--interval', help='interval',
                        default=5, type=int, required=False, metavar='seconds',
                        dest='interval')
    # Process command line arguments.
    args = parser.parse_args()

    # If both or none of 'url' and 'command' given display help and exit.
    if (args.url == '') == (args.command == ''):
        parser.print_help()
        sys.exit(1)

    req = None
    if args.url != '':
        req = json_request_url(args.url)
    else:
        req = json_request_command(args.command)
    poll_loop(args.interval, req)

if __name__ == "__main__":
    main()
