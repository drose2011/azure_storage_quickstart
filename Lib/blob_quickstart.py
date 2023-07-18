import os

from azure.storage.blob import BlobServiceClient, ContentSettings

def auth_blob_client() -> BlobServiceClient:
    connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    blob_client = BlobServiceClient.from_connection_string(connect_str)

    return blob_client

# Azure location
containter_name = 'intern-blob-quickstart'
azure_file = 'test.txt'

# Local location
local_file = 'assets/test.txt'

# Azure client
blob_client = auth_blob_client()

blob_container_client = blob_client.get_container_client(container=containter_name)
if not blob_container_client.exists():
    blob_container_client.create_container()

with open(local_file, 'rb') as data:
    blob_container_client.upload_blob(name=azure_file, data=data, overwrite=True)

blob_file_client = blob_client.get_blob_client(containter_name, azure_file)
blob_file_client.set_http_headers(ContentSettings(content_type='text/plain'))
