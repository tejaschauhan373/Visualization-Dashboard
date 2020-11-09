from azure.storage.file import FileService
from azure.storage.file import ContentSettings
from pathlib import Path
from games_of_data.config import *
import os

file_service = FileService(account_name=azure_storage_account_name,
                           account_key=azure_storage_access_key)


def get_file_from_path(azure_share_name: str, azure_directory_name: str, azure_file_name: str,
                       absolute_path_of_directory: str, file_name_with_extension: str):
    file_service.get_file_to_path(azure_share_name, azure_directory_name, azure_file_name, absolute_path_of_directory,
                                  file_name_with_extension)
