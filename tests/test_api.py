import unittest
from unittest.mock import (
    patch,
    mock_open,
    MagicMock
)
from luks.config import TestConfig
import luks.api as lapi
from loguru import logger
from tests.common import make_patcher
from tests.mocks.mock_hosts import mock_etc_hosts
from tests.mocks.mock_secrets import MockEntry


class TestAPI(unittest.TestCase):
    """Tests the Luks app"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.log = logger
        with patch('builtins.open', mock_open(read_data=mock_etc_hosts)):
            app = lapi.create_app(config_class=TestConfig)
            cls.app = app.test_client()

    def setUp(self) -> None:
        mock1 = MockEntry('test_entry', 'user', 'password123!', {'my_attr': 'lol'})
        self.mock_secrets = make_patcher(self, 'luks.api.keys.Secrets')()
        self.mock_secrets.db.entries = [
            mock1
        ]
        self.mock_secrets.get_entry.return_value = mock1
        # self.mock_secret_key = make_patcher(self, 'luks.config.get_local_secret_key')
        # self.mock_secret_key.return_value = 'lolthisisasecret3'

    def test_home_page(self):
        resp = self.app.get('/', follow_redirects=True)
        self.assertEqual(resp.status_code, 200)

    def test_get_all_keys(self):
        cases = {
            'api_norm': {
                'path': '/api/keys',
                'code': 200,
                'contenttype': 'application/json',
                'is_json': True
            },
            'norm': {
                'path': '/keys',
                'code': 200,
                'contenttype': 'text/html; charset=utf-8',
                'is_json': False
            }
        }
        for scen, cdict in cases.items():
            self.log.debug(f'Working on case {scen}')
            resp = self.app.get(cdict['path'], follow_redirects=True)
            self.assertEqual(resp.status_code, cdict['code'])
            self.assertEqual(resp.is_json, cdict['is_json'])
            if cdict['is_json']:
                self.assertGreaterEqual(len(resp.json.get('data')), 1)
            self.assertEqual(resp.content_type, cdict['contenttype'])

    def test_get_key(self):
        resp = self.app.get('/api/key/test_entry', follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        resp = self.app.get('/key/test_entry', follow_redirects=True)
        self.assertEqual(resp.status_code, 200)

    def test_get_all_hosts(self):
        resp = self.app.get('/api/hosts', follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        resp = self.app.get('/hosts', follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
