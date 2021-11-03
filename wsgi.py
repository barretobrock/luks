import logging
from flask import has_request_context, request
from flask.logging import default_handler
from kavalkilu import LogWithInflux
from luks import ProductionConfig
from luks.api import create_app


log = LogWithInflux('luks-wsgi')
app = create_app(config_class=ProductionConfig)


class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.remote_addr = None
        return super().format(record)


# Instantiate log here, as the hosts API is requested to communicate with influx
formatter = RequestFormatter('[%(asctime)s] %(remote_addr)s requested %(url)s\n'
                             '%(levelname)s in %(module)s: %(message)s')
default_handler.setLevel(level='DEBUG')
default_handler.setFormatter(formatter)
log.log_obj.addHandler(default_handler)

if __name__ == '__main__':
    app.run()
