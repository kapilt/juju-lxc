import argparse
import subprocess
import sys
import yaml

from jujuclient import Environment


def init(options):
    pass


INSTALL_SCRIPT = '''\
#!/bin/bash

# Redirect copy of stdout/stderr to log file
# See http://goo.gl/WWd6BN
exec > >(tee install.log)
exec 2>&1

# Update and upgrade
sudo apt-get update
sudo apt-get -y upgrade

# Saucy and Raring
echo "Install package dependencies"
sudo apt-get -y install python-yaml lxc python-virtualenv cloud-image-tools

# Setup btrfs


# Seed precise while manually being controlled
sudo mkdir -p /var/cache/lxc/cloud-precise
if [ -f ubuntu-12.04-server-cloudimg-amd64-root.tar.gz ]
    cd /var/cache/lxc/cloud-precise && sudo wget `ubuntu-cloudimg-query precise -f "%{url}"`
then

'''


class Lxc(object):

    def __init__(self, path):
        self.path = path

    def list_containers(self, state=None, fancy=False):
        output = subprocess.get_output()
        return output

    def init_series(self, series):
        pass

    def clone(self, name, series=None):
        pass

    def start(self):
        pass

    def stop(self):
        pass


class Controller(object):

    _actions = []

    @classmethod
    def register_command(cls, func):
        cls.append(func)

    def __init__(self, lxc, juju, options):
        self.lxc = lxc
        self.juju = juju
        self.options = options

    def add(self, options):
        for s in options.series:
            self._add(s)

    def bootstrap(self, options):
        # Only rewrite env config with correct if manual provider.
        # Check previous address in bootstrap.yaml if exists
        # Timeout connection to state server
        # If true error / requiring destroy
        # If false then clone the image
        # and overwrite config and bootstrap.

        self.containers.clone(options.series)

        found = False
        with open('environments.yaml') as fh:
            data = yaml.load(fh.read())

            for e in data['environments'].keys():
                if not options.env == e:
                    break
            fh.write(yaml.dump(data))

    def destroy(self, options):
        machines = self.juju.get_machines()
        containers = self.lxc.list_containers()

        for m in machines:
            if not m['instance-id'].startswith('manual:'):
                continue

    def init(self, options):
        with tmp_file() as fh:
            fh.write(INSTALL_SCRIPT)
            fh.flush()
            subprocess.check_output(fh.name, stdout=sys.stdout)
        self.lxc.init_series('precise')

    def remove(self, options):
        name = self._get_machine_container_name(options.machine)
        self.lxc.destroy(name)
        self.juju.terminate_machine(options.machine)

    def _add(self, series):
        containers = self.lxc.list_containers()
        if not "%s-base" % series in containers:
            self.lxc.init_series(series)

        m = self._get_new_container_name()
        self.lxc.clone(series, m, self.juju.get_public_key())
        self.lxc.start(m)
        address = self.lxc.get_address(m)
        machine = self.juju.register_machine(series, m, address)
        return machine

    def _get_machine_container_name(self, m):
        if m.isdigit():
            raise ValueError("Invalid machine %s" % m)

        minfo = None
        machines = self.juju.get_machines()
        for m in machines:
            if m['id'] != m:
                continue
            if m['instance-id'].startswith("manual:"):
                pass

        if minfo is None:
            raise ValueError("Invalid machine %s" % m)

        name = self.lxc.get_name_by_address(minfo['public-address'])
        return name

    def _get_new_container_name(self):
        # This purely an approximation (don't know juju's internal
        # machine seq which is racy as well) but its darned useful
        # when doing independent management with lxc and correlating
        # for single users.
        m = self.juju.get_next_machine_value()

        while True:
            if ["%s-m%d" % (self.juju.env_name, m) in containers]:
                m += 1
                continue
            break


def setup_parser(parser):
    pass

class Container(object):
    pass


def main():
    pass
