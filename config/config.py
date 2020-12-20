# database
from configparser import ConfigParser, ExtendedInterpolation

config = ConfigParser(interpolation=ExtendedInterpolation())
config.read('config/db_config.ini', encoding='utf-8-sig')
DB_PATH = config['database']['db_url']


DIR_FILE = 'config/dir_path.ini'
DIR_CONFIG = ConfigParser()
DIR_CONFIG.read(DIR_FILE)

DATA_PATH = DIR_CONFIG['DIR']['DATA_PATH']
