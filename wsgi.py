from kavalkilu import LogWithInflux
from luks import ProductionConfig
from luks.api import create_app


log = LogWithInflux('luks-wsgi')
app = create_app(config_class=ProductionConfig)


if __name__ == '__main__':
    # Instantiate log here, as the hosts API is requested to communicate with influx
    app.run()
