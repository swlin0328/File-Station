import os
import pandas as pd

from tqdm import tqdm
from lib.nas.file_station import Filestation_Config
from lib.db.sql_connect import SQL_Config

class Dataset_Download(SQL_Config):
    """
    Download the dataset from SQL
    """
    def __init__(self, dataset_name, saved_path, user=None, password=None, database=None, host_address=None, db_url=None, port=32769):
        super().__init__(user, password, database, host_address, db_url, port)
        self.filestation = Filestation_Config(user, password, host_address)
        self.saved_path = saved_path
        
        self.dataset_name = dataset_name
        self.postgreSQL_connect()

    def download_label(self, sql_query=None):
        if sql_query is None:
            sql_query = 'SELECT * FROM "Image_Label" WHERE "Dataset"=\'' + self.dataset_name + '\';'
            
        file_name = self.dataset_name + '_label_data'
        label_df = self.download_sql_table(sql_query, file_name)
        return label_df

    def download_BBoxes(self, sql_query=None):
        if sql_query is None:
            sql_query = 'SELECT * FROM "Image_Annot" WHERE "Dataset"=\'' + self.dataset_name + '\';'
            
        file_name = self.dataset_name + '_bboxes_data'
        bboxes_df = self.download_sql_table(sql_query, file_name)
        return bboxes_df
        
    def download_imageInfo(self, sql_query=None):  
        if sql_query is None:
            sql_query = 'SELECT * FROM "Image_Info" WHERE "Dataset"=\'' + self.dataset_name + '\';'
            
        file_name = self.dataset_name + '_image_info'
        image_df = self.download_sql_table(sql_query, file_name)
        return image_df
    
    def download_image(self, dataset_df, image_df): 
        path = dataset_df.set_index('Name').loc[self.dataset_name, 'Prefix_Path']
        img_files = image_df.set_index('Dataset').loc[self.dataset_name, 'File_Name']
        dst_dir = self.saved_path + 'image/' + self.dataset_name
        print('Start download image...')
        
        for file_name in tqdm(img_files, ncols=60):
            self.filestation.download_file(path, file_name, dst_dir)
            
        print('All the images are downloaded')
        
    def download_datasetInfo(self, sql_query=None):
        if sql_query is None:
            sql_query = 'SELECT * FROM "Dataset" WHERE "Name"=\'' + self.dataset_name + '\';'
            
        file_name = self.dataset_name + '_dataset'
        dataset_df = self.download_sql_table(sql_query, file_name)
        return dataset_df
        
    def download_sql_table(self, sql_query, file_name):
        if not os.path.exists(self.saved_path):
            os.makedirs(self.saved_path)
            
        print('Start to query...')
        table_df = pd.read_sql(sql_query, self.db)
        table_df.to_csv(self.saved_path + file_name + '.csv', index=False, encoding='utf_8_sig')
        print('==> The ' + file_name + '.csv is saved \n')
            
        return table_df
        
    def start(self):
        label_df = self.download_label()
        bboxes_df = self.download_BBoxes()
        image_df = self.download_imageInfo()
        dataset_df = self.download_datasetInfo()
        
        self.download_image(dataset_df, image_df)