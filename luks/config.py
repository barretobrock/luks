"""Configuration setup"""
import pathlib

from luks import (
    __update_date__,
    __version__,
)


def get_local_secret_key(path: pathlib.Path) -> str:
    """Grabs a locally-stored secret"""
    if not path.exists():
        raise FileNotFoundError(f'The luks secret key was not found at path: {path}')
    with path.open() as f:
        return f.read().strip()


class BaseConfig(object):
    """Configuration items common across all config types"""
    DEBUG = False
    TESTING = False
    VERSION = __version__
    UPDATE_DATE = __update_date__
    path = pathlib.Path()
    PORT = 5006
    # Stuff for frontend
    STATIC_DIR_PATH = '../static'
    TEMPLATE_DIR_PATH = '../templates'
    # backend
    DATA_DIR = path.home().joinpath('data')
    KEY_DIR = path.home().joinpath('keys')
    SECRET_KEY_PATH = KEY_DIR.joinpath('luks-secret')
    SECRET_KEY = get_local_secret_key(SECRET_KEY_PATH)


class DevelopmentConfig(BaseConfig):
    """Configuration for development environment"""
    DEBUG = True
    DB_SERVER = 'localhost'
    LOG_LEVEL = 'DEBUG'


class ProductionConfig(BaseConfig):
    """Configuration for production environment"""
    DEBUG = False
    DB_SERVER = '0.0.0.0'
    LOG_LEVEL = 'DEBUG'


class TestConfig(BaseConfig):
    """Configuration for development environment"""
    DEBUG = False
    TESTING = True
    WTF_CSRF_ENABLED = False
    DB_SERVER = 'localhost'
    LOG_LEVEL = 'DEBUG'
