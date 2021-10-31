from kavalkilu import LogWithInflux
from luks import ProductionConfig
from luks.api import create_app


if __name__ == '__main__':
    # Instantiate log here, as the hosts API is requested to communicate with influx
    log = LogWithInflux('luks-api')
    config = ProductionConfig
    app = create_app(config_class=config)
    app.run(host=config.DB_SERVER, port=config.PORT)
