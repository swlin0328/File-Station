# database
from configparser import ConfigParser, ExtendedInterpolation

config = ConfigParser(interpolation=ExtendedInterpolation())
config.read('./config/db_config.ini', encoding='utf-8-sig')

db_info = config['database']
host_ip = db_info['host_ip']
port = db_info['port']
user_name = db_info['user_name']
password = db_info['password']
db_name = db_info['db_name']
db_url = db_info['db_url']

dataset_path = config['dataset']['dir_path']
saved_path = config['dataset']['saved_path']
