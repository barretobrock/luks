"""Configuration setup"""
import pathlib
from ._version import get_versions


class BaseConfig(object):
    """Configuration items common across all config types"""
    _v = get_versions()
    VERSION = _v['version']
    UPDATE_DATE = _v['date']
    path = pathlib.Path
    PORT = 5006
    # Stuff for frontend
    STATIC_DIR_PATH = '../static'
    TEMPLATE_DIR_PATH = '../templates'
    # backend
    DATA_DIR = path.home().joinpath('data')
    KEY_DIR = path.home().joinpath('keys')
    SECRET_KEY_PATH = KEY_DIR.joinpath('luks-secret')
    if not SECRET_KEY_PATH.exists():
        raise FileNotFoundError(f'luks-secret at {SECRET_KEY_PATH} not found...')
    with SECRET_KEY_PATH.open() as f:
        SECRET_KEY = f.read().strip()


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
