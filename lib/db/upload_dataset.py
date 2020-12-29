from sqlalchemy import exc
from lib.nas.dsm_config import NAS_Config
from lib.nas.file_station import Filestation_Config
from lib.db.sql_connect import SQL_Config
from tqdm import tqdm

class Image_Dataset2DB(SQL_Config):
    """
    Upload the public dataset information to SQL
    """
    def __init__(self, user=None, password=None, database=None, host_address=None, db_url=None, port=32769):
        super().__init__(user, password, database, host_address, db_url)
        self.connect2NAS()
        
    def connect2NAS(self):
        self.dsm_api = NAS_Config(self.user, self.password, self.host)
        self.filestation_api = Filestation_Config(self.user, self.password, self.host)
        
        print('connct to NAS...')    
        self.dsm_api.print_utilisation()
        self.dsm_api.print_system_info()

    def upload_label(self, label_df):
        print('start to upload label...')
        self.upload_dataset2sql(label_df, "Image_Label")    

    def upload_BBoxes(self, annot_df):
        print('start to upload BBox...')
        self.upload_dataset2sql(annot_df, "Image_Annot")  
        
    def upload_imageInfo(self, image_df):  
        print('start to upload image info...')
        self.upload_dataset2sql(image_df, "Image_Info")
        
    def upload_datasetInfo(self, dataset_df):
        print('start to upload dataset info...')
        self.upload_dataset2sql(dataset_df, "Dataset")      
            
    def upload_dataset2sql(self, df, table_name, if_exists='append'):
        for idx in tqdm(range(len(df)), ncols=60):
            try:
                df.iloc[idx:idx+1].to_sql(table_name, self.engine, if_exists=if_exists, index=False)
            except exc.IntegrityError:
                pass