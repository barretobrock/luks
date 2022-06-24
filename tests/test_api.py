import unittest
from unittest.mock import (
    patch,
    mock_open,
    MagicMock
)
from loguru import logger
from tests.common import make_patcher
from tests.mocks.mock_hosts import mock_etc_hosts


class TestAPI(unittest.TestCase):
    """Tests the Luks app"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.log = logger

    def setUp(self) -> None:
        self.mock_secret_key = make_patcher(self, 'luks.config.get_local_secret_key')
        self.mock_secret_key.return_value = 'lolthisisasecret3'

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
