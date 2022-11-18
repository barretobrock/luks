from datetime import datetime
import enum
import os.path
import re
from typing import (
    Dict,
    List,
)


class HostnameNotFoundException(Exception):
    pass


class IPAddressNotFoundException(Exception):
    pass


class MachineType(enum.Enum):
    laptop = enum.auto()
    desktop = enum.auto()
    server = enum.auto()
    raspi = enum.auto()
    camera = enum.auto()
    mobile = enum.auto()
    peripheral = enum.auto()
    other = enum.auto()


class ServerHosts:
    """Everything associated with the Hosts API"""
    def __init__(self):
        self.all_hosts = []
        # Populate the hosts list for the first time
        self.read_hosts()

    @staticmethod
    def _map_name_to_machine_type(name: str) -> MachineType:
        prefix = name.split('-')[0]
        if prefix in ['ac', 're']:
            return MachineType.camera
        elif prefix == 'lt':
            return MachineType.laptop
        elif prefix == 'pc':
            return MachineType.desktop
        elif prefix == 'ot':
            return MachineType.peripheral
        elif prefix == 'pi':
            return MachineType.raspi
        elif prefix == 'an':
            return MachineType.mobile
        elif 'serv' in name:
            return MachineType.server
        else:
            return MachineType.other

    @staticmethod
    def get_hosts_modified_time() -> datetime:
        return datetime.fromtimestamp(os.path.getmtime('/etc/hosts'))

    def read_hosts(self):
        """Reads in /etc/hosts, parses data"""
        with open('/etc/hosts', 'r') as f:
            hostlines = f.readlines()
        hostlines = [re.split(r'\s+', line.strip()) for line in hostlines if line.startswith('192.168')]
        hosts = []
        for ip, name in hostlines:
            mach_type = self._map_name_to_machine_type(name)

            hosts.append({
                'ip': ip.strip(),
                'name': name.strip(),
                'machine_type': mach_type.name
            })
        self.all_hosts = hosts

    def reload(self):
        """Reloads the hosts"""
        self.read_hosts()

    def get_all_names(self) -> List[str]:
        """Returns a list of all the names"""
        return [x['name'] for x in self.all_hosts]

    def get_all_ips(self) -> List[str]:
        """Returns a list of all the ips"""
        return [x['ip'] for x in self.all_hosts]

    def get_host(self, ip: str) -> Dict[str, str]:
        """Returns ip from host name"""
        for host in self.all_hosts:
            if host['ip'] == ip:
                return host
        raise HostnameNotFoundException(f'Hostname not found for ip {ip}.')

    def get_ip(self, hostname: str) -> Dict[str, str]:
        """Returns ip from host name"""
        for host in self.all_hosts:
            if host['name'] == hostname:
                return host
        raise IPAddressNotFoundException(f'IP address not found for hostname {hostname}.')
