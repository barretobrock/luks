from datetime import (
    datetime,
    timedelta,
)
from random import randint
from typing import Dict


class MockEntry:
    def __init__(self, title: str, un: str = None, pw: str = None, custom_props: Dict = None):
        self.title = title
        self.username = un
        self.password = pw
        self.custom_properties = custom_props
        self.attachments = []
        self.mtime = (datetime.now() - timedelta(seconds=randint(50, 50000)))
