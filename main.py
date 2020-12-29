from lib.utils.config import db_info, host_ip, port, user_name , password, db_name, db_url, dataset_path, saved_path
from lib.db.download_dataset import Dataset_Download
from lib.db.create_table import Table_Creator
from lib.utils.voc_dataset import VOC_Dataset
from lib.nas.dsm_config import NAS_Config
from lib.nas.file_station import Filestation_Config

import warnings

def query_NAS():
	dsm_api = Filestation_Config(user_name, password, host_ip)
	dsm_api.print_shared_folder()

def create_table4imageDB():
	Table_Creator(user=user_name, password=password, database=db_name, host_address=host_ip, port=port).start()

def upload_voc_dataset():
	prefix = dataset_path.split('/')[-2]
	voc = VOC_Dataset(dataset_path, prefix,
					user=user_name, password=password, database=db_name, host_address=host_ip, port=port)
					
	voc.postgreSQL_connect()
	label_dict = voc.create_label_ID(saved_path + 'label/VOC2007.txt')
	voc.extract_label_info()
	voc.extract_dataset_info(nas_path='/dataset')

def download_voc_dataset():
	Dataset_Download('VOC2007', saved_path, user=user_name, password=password, database=db_name, host_address=host_ip, port=port).start()

if __name__ == '__main__':
	warnings.filterwarnings("ignore")
	query_NAS()
	create_table4imageDB()
	upload_voc_dataset()
	download_voc_dataset()
