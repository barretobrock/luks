import pathlib
from pukr import get_logger
from luks.config import ProductionConfig
from luks.api import create_app

app = create_app(config_class=ProductionConfig)

if __name__ == '__main__':
    log = get_logger(log_name='luks-api', log_dir_path=pathlib.Path().home().joinpath('logs/luks'))
    app.run(host=ProductionConfig.DB_SERVER, port=ProductionConfig.PORT)
