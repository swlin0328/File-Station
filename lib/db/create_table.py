from lib.db.sql_connect import SQL_Config
from sqlalchemy import Table, Column, MetaData, Integer, Computed, String

class Table_Creator(SQL_Config):
    """
    Create SQL Table with sqlalchemy
    """
    def __init__(self, user=None, password=None, database=None, host_address=None, db_url=None, port=32769):
        super().__init__(user, password, database, host_address, db_url, port)

    def create_table4annot(self):
        metadata = MetaData()

        data = Table(
            "Image_Annot", metadata,
            Column('UUID', Integer, autoincrement=True, primary_key=True),
            Column('Name', String),
            Column('Pose', String),
            Column('Truncated', Integer),
            Column('Difficult', Integer),
            Column('Xmin', Integer),
            Column('Ymin', Integer),
            Column('Xmax', Integer),
            Column('Ymax', Integer),
            Column('File', String),
            Column('Dataset', String)
            )
        metadata.create_all(self.engine)

    def create_table4label(self):
        metadata = MetaData()

        data = Table(
            "Image_Label", metadata,
            Column('Label_ID', Integer),
            Column('Name', String, primary_key=True),
            Column('Dataset', String, primary_key=True)
            )

        metadata.create_all(self.engine)
        
    def create_table4image(self):
        metadata = MetaData()

        data = Table(
            "Image_Info", metadata,
            Column('File_Name', String, primary_key=True),
            Column('Width', Integer),
            Column('Height', Integer),
            Column('Depth', Integer),
            Column('Dataset', String, primary_key=True)
            )

        metadata.create_all(self.engine)
        
    def create_table4dataset(self):
        metadata = MetaData()

        data = Table(
            "Dataset", metadata,
            Column('Name', String),
            Column('Prefix_Path', String, primary_key=True),
            )

        metadata.create_all(self.engine)
        
    def start(self):
        self.postgreSQL_connect()
        
        self.create_table4annot()
        self.create_table4label()
        self.create_table4image()
        self.create_table4dataset()