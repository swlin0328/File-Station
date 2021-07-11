import os
import pandas as pd
import xml.etree.ElementTree as XET

from lib.db.upload_dataset import Image_Dataset2DB
from tqdm import tqdm

class VOC_Dataset(Image_Dataset2DB):
    """
    Extract information of VOC dataset
    """
    def __init__(self, dir_path, dataset_name, 
                 user=None, password=None, database=None, host_address=None, db_url=None, port=32769):
        self.dataset_name = dataset_name
        self.dir_path = dir_path
        
        super().__init__(user, password, database, host_address, db_url)
        
    def extract_dataset_info(self, nas_path):
        dataset_df = pd.DataFrame([], columns=["Name", "Prefix_Path"])
        dir_dict = self.filestation_api.query_dir_info(nas_path)
        print('query dataset info from NAS...')
    
        for folder_name in dir_dict.keys():
            if self.dataset_name == folder_name:
                dataset_df = dataset_df.append({"Name": folder_name, "Prefix_Path": dir_dict[folder_name]},
                                           ignore_index=True)
                
        self.upload_datasetInfo(dataset_df)
    
    def extract_label_info(self):
        path = self.dir_path + 'Annotations/'
        bbox_df = pd.DataFrame([], columns=["Name", "Pose", "Truncated", "Difficult",
                                             "Xmin", "Ymin", "Xmax", "Ymax",
                                             "File", "Dataset"])
        image_df = pd.DataFrame([], columns=["File_Name", "Width", "Height", "Depth", "Dataset"])
    
        file_list = os.listdir(path)
        print('start to extract lable info...')
    
        for file in tqdm(file_list, ncols=60):
            tree = XET.parse(path + file)
            root = tree.getroot()
            dataset = root.findall('folder')[0].text

            if self.dataset_name != dataset:
                continue
        
            file_name = root.findall('filename')[0].text
            size = root.findall('size')[0]
        
            width = int(size[0].text)
            height = int(size[1].text)
            depth = int(size[2].text)
        
            image_df = image_df.append({"File_Name": file_name,
                                        "Width": width,
                                        "Height": height,
                                        "Depth": depth,
                                        "Dataset": self.dataset_name},
                                       ignore_index=True)
            bbox_df = self.extract_BBoxes(root, bbox_df, file_name)    
            
        self.upload_imageInfo(image_df)
        self.upload_BBoxes(bbox_df)
        
    def extract_BBoxes(self, root, bbox_df, file_name):
        objects = root.findall('object')
    
        for obj in objects:
            name = obj.find('name').text
            pose = obj.find('pose').text

            try:
                truncated = obj.find('truncated').text
                difficult = obj.find('difficult').text
            except:
                truncated = 0
                difficult = 0
            
            bndbox = obj.find('bndbox')
            xmin = int(bndbox[0].text)
            ymin = int(bndbox[1].text)
            xmax = int(bndbox[2].text)
            ymax = int(bndbox[3].text)
        
            bbox_df = bbox_df.append({"Name": name, 
                                      "Pose": pose, 
                                      "Truncated": truncated, 
                                      "Difficult": difficult, 
                                      "Xmin": xmin, 
                                      "Ymin": ymin, 
                                      "Xmax": xmax, 
                                      "Ymax": ymax, 
                                      "File": file_name, 
                                      "Dataset": self.dataset_name}, 
                                     ignore_index=True)
        return bbox_df
    
    def create_label_ID(self, label_path):
        label_df = pd.DataFrame([], columns=["Label_ID", "Name", "Dataset"])
        print('create label ID...')

        with open(label_path, "r") as f:
            lines = f.read().splitlines()
            for idx, line in enumerate(lines):
                label_df = label_df.append({"Label_ID": idx, "Name": line, "Dataset": self.dataset_name}, ignore_index=True)

            self.upload_dataset2sql(label_df, "Image_Label")
        
        label_dict = label_df.set_index('Name').to_dict()
        return label_dict["Label_ID"]