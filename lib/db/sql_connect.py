import sqlalchemy as sqlc
from time import strftime

class SQL_Config():
    """
    SQL SERVER 連接設定
    """
    def __init__(self, user=None, password=None, database=None, host_address=None, db_url=None, port=32769):
        self.user = user
        self.password = password
        self.db_name = database
        self.host = host_address
        self.created_time = strftime('%Y-%m-%d %H:%M:%S')
        self.port = port
        
        if db_url is None:
            self.db_url = f"{user}:{password}@{host_address}:{port}/{database}"
        else:
            self.db_url = db_url

    def postgreSQL_connect(self):
        """
        進行 SQL SERVER 連接
        """
        print('=====================================================')
        print('======== Connect to the remote postgre SQL server ========')
        print('=====================================================')
        print('Time : {}\n'.format(strftime('%Y-%m-%d_%H_%M')))
        
        sql_prefix = "postgresql+psycopg2://" + self.db_url
            
        self.engine = sqlc.create_engine(sql_prefix)
        self.db = self.engine.raw_connection()
        self.cursor = self.db.cursor()

    def commit(self):
        """
        資料庫commit
        """
        try:
            trans = self.db
            trans.commit()
        except:
            trans.rollback()

    def disconnect(self):
        """
        資料庫離線
        """
        self.db.close()
        print('=====================================================')
        print('============ Close the remote connection ============')
        print('=====================================================')