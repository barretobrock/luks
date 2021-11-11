from .config import (
    DevelopmentConfig,
    ProductionConfig,
    TestConfig,
    BaseConfig
)
from . import _version
__version__ = _version.get_versions()['version']
