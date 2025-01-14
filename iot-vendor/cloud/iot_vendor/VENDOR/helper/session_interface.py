from secrets_manager import SecretManager
from path_handler import PathHandler

class SecretFacade:
    def __init__(self, secret_arn, region):
        self.secret_manager = SecretManager(
                                    region=region,
                                    secret_manager_key=secret_arn
                                )
        self.path_finder = PathHandler()
        
    def get_db_string(self, vendor_name):
        return self.secret_manager.get_db_string(vendor_name=vendor_name)

    def get_vendor_name(self,path):
        return self.path_finder.get_vendor_name(path=path)    
