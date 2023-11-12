from flask import Flask

from luks.api.hosts import hosts
from luks.api.keys import keys
from luks.api.main import main
from luks.config import ProductionConfig
from luks.hosts import ServerHosts


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

    app.config['svr_host_obj'] = ServerHosts()

    return app
