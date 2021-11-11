import unittest
from unittest.mock import (
    patch,
    MagicMock
)
from easylogger import Log
from luks.secrets import Secrets


class TestSecrets(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.log = Log('test-secrets')

    @patch('luks.secrets.pykeepass.PyKeePass')
    def test_init_secrets(self, mock_keepass: MagicMock):
        secrets = Secrets('something')
        mock_keepass.assert_called_once()

    @patch('luks.secrets.pykeepass.PyKeePass')
    def test_get_entry(self, mock_keepass: MagicMock):
        secrets = Secrets('something')
        mock_keepass.assert_called_once()
        secrets.get_entry('entry')
