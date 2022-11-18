import pathlib

from pukr import get_logger

from luks.api import create_app
from luks.config import DevelopmentConfig

if __name__ == '__main__':
    # Instantiate log here, as the hosts API is requested to communicate with influx
    log = get_logger(log_name='luks-api', log_dir_path=pathlib.Path().home().joinpath('logs/luks'))
    app = create_app(config_class=DevelopmentConfig)
    app.run(host=DevelopmentConfig.DB_SERVER, port=DevelopmentConfig.PORT)
