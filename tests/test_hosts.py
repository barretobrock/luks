import unittest
from unittest.mock import (
    patch,
    mock_open
)
from loguru import logger
from luks.hosts import (
    ServerHosts,
    HostnameNotFoundException,
    IPAddressNotFoundException
)
from .mocks.mock_hosts import mock_etc_hosts


class TestHosts(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.log = logger

    def test_read_hosts(self):
        with patch('builtins.open', mock_open(read_data=mock_etc_hosts)):
            hosts = ServerHosts()
        self.assertTrue(len(hosts.all_hosts) > 5)
        ip_list = [x.get('ip') for x in hosts.all_hosts]
        self.assertNotIn('192.168.1.100', ip_list)
        self.assertIn('192.168.1.5', ip_list)

    def test_get_host_and_get_ip(self):
        with patch('builtins.open', mock_open(read_data=mock_etc_hosts)):
            hosts = ServerHosts()
        expected_dict = {
            'ip': '192.168.1.8',
            'name': 'servmach',
            'machine_type': 'server'
        }
        self.assertEqual(expected_dict, hosts.get_host('192.168.1.8'))
        self.assertEqual(expected_dict, hosts.get_ip('servmach'))
        with self.assertRaises(HostnameNotFoundException):
            hosts.get_host('192.168.5.5')

        with self.assertRaises(IPAddressNotFoundException):
            hosts.get_ip('swerver')
