#!/usr/bin/env python

# if ansible is pointed to the executable file
# it will execute it to get host information dynamically

# Executable inventory script shoud have
# two CLI arguments:
# * --host=<hostname>
# * --list

import sys
import json
import argparse
import subprocess

import paramiko


def list_running_hosts():
    cmd = ["vagrant", "status", "--machine-readable"]
    status = subprocess.check_output(cmd).rstrip()
    hosts = []
    for line in status.split('\n'):
        _, host, key, value = line.split(',')
        if key == 'state' and value == 'running':
            hosts.append(host)
    return hosts


def get_host_ssh_info(host):
    cmd = ["vagrant", "ssh-config", host]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    config = paramiko.SSHConfig()
    config.parse(p.stdout)
    c = config.lookup(host)
    return {
        'ansible_ssh_host': c['hostname'],
        'ansible_ssh_port': c['port'],
        'ansible_ssh_user': c['user'],
        'ansible_ssh_private_key_file': c['identityfile'][0]
    }


def parse_args():
    parser = argparse.ArgumentParser(description="Vagrant dynamic host information")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--list', action="store_true", description="List vagrant hosts information")
    group.add_argument('--host', description="Show host information")
    return parser.parse_args()


def main():
    args = parse_args()


if __name__ == '__main__':