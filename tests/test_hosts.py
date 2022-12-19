import unittest
from unittest.mock import (
    mock_open,
    patch,
)

from loguru import logger

from luks.hosts import (
    HostnameNotFoundException,
    IPAddressNotFoundException,
    ServerHosts,
)

from .mocks.mock_hosts import mock_etc_hosts


class TestHosts(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.log = logger

    def test_read_hosts(self):
        with patch('pathlib.Path.open', mock_open(read_data=mock_etc_hosts)):
            hosts = ServerHosts()
        self.assertTrue(len(hosts.all_hosts) > 5)

        test_dict = {
            'ip': '192.168.8.5',
            'name': 'an-jam235',
            'machine_type': 'mobile'
        }
        self.assertDictEqual(hosts.get_host(test_dict['ip']), test_dict)
        with self.assertRaises(HostnameNotFoundException):
            hosts.get_host('192.168.7.2')

    def test_get_host_and_get_ip(self):
        with patch('pathlib.Path.open', mock_open(read_data=mock_etc_hosts)):
            hosts = ServerHosts()
        expected_dict = {
            'ip': '192.168.8.8',
            'name': 'servmach',
            'machine_type': 'server'
        }
        self.assertEqual(expected_dict, hosts.get_host(expected_dict['ip']))
        self.assertEqual(expected_dict, hosts.get_ip(expected_dict['name']))
        with self.assertRaises(HostnameNotFoundException):
            hosts.get_host('192.168.5.5')

        with self.assertRaises(IPAddressNotFoundException):
            hosts.get_ip('swerver')
