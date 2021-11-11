import unittest
from unittest.mock import (
    patch,
    mock_open
)
from luks import TestConfig
import luks.api as lapi
from .mocks.mock_hosts import mock_etc_hosts


class TestAPI(unittest.TestCase):
    """Tests the Luks app"""

    @classmethod
    def setUpClass(cls) -> None:
        with patch('builtins.open', mock_open(read_data=mock_etc_hosts)):
            app = lapi.create_app(config_class=TestConfig)
            cls.app = app.test_client()

    def test_home_page(self):
        resp = self.app.get('/', follow_redirects=True)
        self.assertEqual(resp.status_code, 200)

    def test_get_all_keys(self):
        resp = self.app.get('/api/keys', follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        resp = self.app.get('/keys', follow_redirects=True)
        self.assertEqual(resp.status_code, 200)

    def test_get_key(self):
        resp = self.app.get('/api/key/felix', follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        resp = self.app.get('/key/felix', follow_redirects=True)
        self.assertEqual(resp.status_code, 200)

    def test_get_all_hosts(self):
        resp = self.app.get('/api/hosts', follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        resp = self.app.get('/hosts', follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
