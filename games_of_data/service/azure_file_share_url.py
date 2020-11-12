from datetime import datetime, timedelta
from azure.storage.fileshare import ShareServiceClient, generate_account_sas, ResourceTypes, AccountSasPermissions
from games_of_data.config import azure_storage_access_key, azure_storage_account_name
sas_token = generate_account_sas(
    account_name=azure_storage_account_name,
    account_key=azure_storage_access_key,
    resource_types=ResourceTypes(service=True),
    permission=AccountSasPermissions(read=True),
    expiry=datetime.utcnow() + timedelta(hours=1)
)

share_service_client = ShareServiceClient(account_url="https://<my_account_name>.file.core.windows.net", credential=sas_token)
