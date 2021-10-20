import pathlib
from typing import Dict
from pykeepass import PyKeePass
from pykeepass.entry import Entry


path = pathlib.Path
KEY_DIR = path.home().joinpath('keys')
PROPS_PATH = KEY_DIR.joinpath('SECRETPROP')
PROPS_DB_PATH = KEY_DIR.joinpath('secretprops.kdbx')


def get_secret_file(fpath: pathlib.PosixPath = PROPS_PATH) -> str:
    """Grabs a file containing a 'metasecret' (secret for obtaining secrets)"""
    if not fpath.exists():
        raise FileNotFoundError(f'File at \'{fpath}\' does not exist.')
    with fpath.open() as f:
        return f.read().strip()


def read_props(fpath: pathlib.PosixPath) -> Dict[str, str]:
    props = {}
    with fpath.open('r') as f:
        contents = f.read().split('\n')
        for item in contents:
            if item != '' and not item.startswith('#'):
                key, value = item.split('=', 1)
                props[key] = value.strip()
    return props


class Secrets:
    def __init__(self, password: str, secrets_db_path: pathlib.PosixPath = PROPS_DB_PATH):
        self.db = None
        self.db_path = secrets_db_path
        # Read in the database
        self.load_database(password)

    def load_database(self, password: str):
        self.db = PyKeePass(self.db_path, password=password)

    def get_entry(self, entry_name: str) -> Entry:
        return self.db.find_entries(title=entry_name, first=True)
