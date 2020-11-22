from azure.storage.file import FileService
from pathlib import Path
from azure.storage.file import ContentSettings
from config import azure_storage_account_name, azure_share_name, azure_storage_access_key
import os

file_service = FileService(account_name=azure_storage_account_name, account_key=azure_storage_access_key)
file_service.create_share(azure_share_name)
print("azure_storage_account_name",azure_storage_account_name, "azure_storage_access_key",azure_storage_access_key)
print("azure_share_name",azure_share_name)

def upload_file_to_azure(directory_name: str, azure_file_name: str, local_file_path: str,
                content_type: str):
    print("Directory exists",file_service.create_directory(azure_share_name, directory_name, metadata=None, fail_on_exist=False))
    file_service.create_file_from_path(
        azure_share_name,
        directory_name,  # We want to create this file in the root directory, so we specify None for the directory_name
        azure_file_name,
        local_file_path,
        content_settings=ContentSettings(content_type=content_type))

def get_file_from_azure(azure_directory_name: str, azure_file_name: str,
                       absolute_file_path_with_extension: str):
    file_service.get_file_to_path(azure_share_name, azure_directory_name, azure_file_name, absolute_file_path_with_extension)


def delete_file_from_azure(azure_directory_name: str, azure_file_name: str):
    file_service.delete_file(azure_share_name, azure_directory_name, azure_file_name)

def get_downloadable_url_of_azure_file(azure_directory_name: str, azure_file_name: str):
    return file_service.generate_file_shared_access_signature(azure_share_name, directory_name=azure_directory_name, file_name=azure_file_name)