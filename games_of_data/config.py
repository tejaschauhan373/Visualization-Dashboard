import os
import json
from os import path

config_file = "example.config.json"

if path.isfile('config.json'):
    config_file = 'config.json'


with open(os.path.join(os.path.join(os.getcwd()),"config.json"), 'r') as configs:
    config_object = json.loads(configs.read())

azure_storage_access_key = config_object["default"]["storage_access_key"]
azure_storage_account_name = config_object["default"]["storage_account_name"]
azure_connection_string = config_object["default"]["azure_connection_string"]
azure_share_name = config_object["default"]["share_name"]
