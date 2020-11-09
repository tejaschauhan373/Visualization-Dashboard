from azure.storage.file import FileService
from azure.storage.file import ContentSettings
from pathlib import Path
from games_of_data.config import *
import os

file_service = FileService(account_name=azure_storage_account_name,
                           account_key=azure_storage_access_key)

file_service.get_file_to_path('test', None, 'myfile_from_root', os.path.join(Path(os.getcwd()).parent, 'myfile.xlsx'))
