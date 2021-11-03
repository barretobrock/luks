from flask import Flask
from easylogger import Log
from luks import ProductionConfig
from .hosts import hosts
from .keys import keys
from .main import main


def create_app(*args, **kwargs) -> Flask:
    """Creates a Flask app instance"""
    # Config app
    config_class = kwargs.pop('config_class', ProductionConfig)
    app = Flask(__name__, static_folder=config_class.STATIC_DIR_PATH, static_url_path='/',
                template_folder=config_class.TEMPLATE_DIR_PATH)
    app.config.from_object(config_class)
    # Register routes
    for rt in [hosts, keys, main]:
        app.register_blueprint(rt)

    return app
