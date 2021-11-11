from unittest.mock import (
    patch,
    mock_open
)
from typing import (
    Dict,
    List,
    Union
)
from pykeepass.entry import Entry


class MockEntry(Entry):
    def __init__(self, title: str, un: str = None, pw: str = None, custom_props: Dict = None,
                 files: Dict[str, Union[str, bytes]] = None):
        super().__init__(title=title, username=un, password=pw)
        if custom_props is not None:
            for k, v in custom_props.items():
                self.set_custom_property(k, v)
        if files is not None:
            for k, v in files.items():
                with patch('builtins.open', mock_open(read_data=v)):
                    self.add_attachment(id=k, filename=f'/tmp/{k}')
