from azure.storage.file import FileService
from pathlib import Path
from azure.storage.file import ContentSettings
from games_of_data.config import azure_storage_account_name, azure_share_name, azure_storage_access_key
import os

file_service = FileService(account_name=azure_storage_account_name, account_key=azure_storage_access_key)
file_service.create_share('test')


def upload_file(share_name: str, directory_name: str, azure_file_name: str, local_file_path: str,
                content_type: str):
    file_service.create_file_from_path(
        share_name,
        directory_name,  # We want to create this file in the root directory, so we specify None for the directory_name
        azure_file_name,
        local_file_path,
        content_settings=ContentSettings(content_type=content_type))
