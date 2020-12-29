from synology_dsm import SynologyDSM
from time import strftime

class NAS_Config():
    """
    Synology DSM 連接設定
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
        print('======== Connect to the remote NAS server ========')
        print('=====================================================')
        print('Time : {}\n'.format(strftime('%Y-%m-%d_%H_%M')))
            
        self.api = SynologyDSM(self.host, self.port, self.user, self.password)

    def print_system_info(self):
        """
        顯示系統資訊
        """
        print("=== Information ===")
        self.api.information.update()
        print("Model:           " + str(self.api.information.model))
        print("RAM:             " + str(self.api.information.ram) + " MB")
        print("Temperature:     " + str(self.api.information.temperature) + " °C")
        print("--")

    def print_utilisation(self):
        """
        顯示資源使用率
        """
        self.api.utilisation.update()
        print("CPU Load:        " + str(self.api.utilisation.cpu_total_load) + " %")
        print("Memory Use:      " + str(self.api.utilisation.memory_real_usage) + " %")
        print("Net Up:          " + str(self.api.utilisation.network_up()))
        print("Net Down:        " + str(self.api.utilisation.network_down()))
        print("--")

    def print_storage_info(self):  
        """
        顯示儲存裝置資訊
        """
        print("=== Storage ===")
        self.api.storage.update()
        for volume_id in self.api.storage.volumes_ids:
            print("ID:          " + str(volume_id))
            print("Status:      " + str(self.api.storage.volume_status(volume_id)))
            print("% Used:      " + str(self.api.storage.volume_percentage_used(volume_id)) + " %")
            print("--")
            
        for disk_id in self.api.storage.disks_ids:
            print("ID:          " + str(disk_id))
            print("Name:        " + str(self.api.storage.disk_name(disk_id)))
            print("Status:      " + str(self.api.storage.disk_status(disk_id)))
            print("Temp:        " + str(self.api.storage.disk_temp(disk_id)))
            print("--")
            
    def print_shared_folder(self):  
        """
        顯示共用空間資訊
        """ 
        print("=== Shared Folders ===")
        self.api.share.update()
        for share_uuid in self.api.share.shares_uuids:
            print("Share name:        " + str(self.api.share.share_name(share_uuid)))
            print("Share path:        " + str(self.api.share.share_path(share_uuid)))
            print("Space used:        " + str(self.api.share.share_size(share_uuid, human_readable=True)))
            print("--")