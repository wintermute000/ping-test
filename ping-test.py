#!/usr/bin/env python

import yaml
import os
import re
from pprint import pprint
from collections import Counter


class ping_test():

    def generate_host_list(self, host_path, host_file):
        # Generate list of hosts to check
        host_list = yaml.load(open(correct_path + '/' + host_file, "r"))
        return sorted(host_list)

    def parse_pings(self, hosts, path, filename):
        DESTINATION_RE = re.compile(r'Echos to ((?:[0-9]{1,3}\.){3}[0-9]{1,3}),')
        SOURCE_RE = re.compile(r'Packet sent with a source address of ((?:[0-9]{1,3}\.){3}[0-9]{1,3})')
        SUCCESS_RE = re.compile(r'Success rate is (\d*) percent')

        for device in hosts:
            file_name = path + "/" + device + "." + filename
            file = open(file_name, 'r')
            ping_contents = file.readlines()
            print ("=============")
            print ('Device - ' + device)

            for line in ping_contents:
                source_raw = re.search(SOURCE_RE, str(line))
                source = source_raw.group(1)
                destination_raw = re.search(DESTINATION_RE, str(line))
                destination = destination_raw.group(1)
                success_raw = re.search(SUCCESS_RE, str(line))
                success = success_raw.group(1)

                if success != '0':
                    print ('Ping from Source ' + source + ' to Destination ' + destination + ' OK')
                else:
                    print ('Ping from Source ' + source + ' to Destination ' + destination + ' FAIL!')


if __name__ == '__main__':

    correct_path = "./host_vars"

    host_path = "./host_vars"
    host_file = "hosts.yml"
    show_path = "./show_outputs"

    ping_filename = "ping.output.txt"

    job = ping_test()
    hosts = job.generate_host_list(host_path,host_file)
    check_pings = job.parse_pings(hosts, show_path, ping_filename)
