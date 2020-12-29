import os
import shutil
import pandas as pd

from synology_api import filestation
from time import strftime

class Filestation_Config():
    """
    Synology Filestation 連接設定
    """
    def __init__(self, user=None, password=None, host_address=None, port="5000"):
        self.user = user
        self.password = password
        self.host = host_address
        self.created_time = strftime('%Y-%m-%d %H:%M:%S')
        self.port = port
        
        self.connect()

    def connect(self):
        """
        連接 Synology NAS 
        """
        print('=====================================================')
        print('======== Connect to the remote filestation ========')
        print('=====================================================')
        print('Time : {}\n'.format(strftime('%Y-%m-%d_%H_%M')))
            
        self.api = filestation.FileStation(self.host, self.port, self.user, self.password)
            
    def print_shared_folder(self):  
        """
        顯示共用空間資訊
        """ 
        print("=== Shared Folders ===")
        query_info = self.api.get_list_share()
        if not query_info['success']:
            print('query shared folder failed...')
            
        for folder_info in query_info['data']['shares']:
            if folder_info['isdir']:
                print(folder_info['name'])
                print(folder_info['path'])
                print('---')
                
    def query_file_list(self, dir_path):  
        """
        顯示資料夾內容
        """ 
        query_info = self.api.get_file_list(dir_path)
        file_df = pd.DataFrame([], columns=["Name", "Path"])
        if not query_info['success']:
            print('query file list failed...')
                
        for folder_info in query_info['data']['shares']:
            print('data list')
            if not folder_info['isdir']:
                print('name: ', folder_info['name'])
                print('path: ', folder_info['path'])
                file_df = file_df.append({"File_Name": folder_info['name'], "File_Path": folder_info['path']}, 
                                         ignore_index=True)
                print('---')
                
        return file_df
    
    def query_dir_info(self, dir_path):  
        """
        顯示資料夾內容
        """ 
        query_info = self.api.get_file_list(dir_path)
        dir_dict = {}
        if not query_info['success']:
            print('query dir list failed...')
            
        for folder_info in query_info['data']['files']:
            print('dir info')
            if folder_info['isdir']:
                print('name: ', folder_info['name'])
                print('path: ', folder_info['path'])
                dir_dict[folder_info['name']] = folder_info['path']
                print('---')
                
        return dir_dict
    
    def download_file(self, path, file_name, dst_path):  
        if not os.path.exists(dst_path):
            os.makedirs(dst_path)
            
        file_path = path + '/' + file_name
        self.api.get_file(file_path, 'download')
        shutil.move(file_name, dst_path)