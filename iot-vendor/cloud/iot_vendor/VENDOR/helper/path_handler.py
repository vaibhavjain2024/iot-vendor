import os
from session_interface import SessionInterface

class PathHandler:
    def get_vendor_name(self, path):
        data = path.split('/')
        return data[data.index('v2')+1]