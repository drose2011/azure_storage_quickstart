import os, uuid

from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient, DataLakeDirectoryClient, FileSystemClient
from azure.storage.blob import BlobServiceClient, ContentSettings, BlobClient, ContainerClient

def get_service_client_token_credential() -> DataLakeServiceClient:
    connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

    service_client = DataLakeServiceClient.from_connection_string(connect_str)

    return service_client

def get_or_make_file_system(service_client: DataLakeServiceClient, file_system_name: str) -> FileSystemClient:
    file_system_client = service_client.get_file_system_client(file_system=file_system_name)

    if not file_system_client.exists():
        file_system_client = service_client.create_file_system(file_system=file_system_name)

    return file_system_client

def get_or_make_directory(file_system_client: FileSystemClient, directory_name: str) -> DataLakeDirectoryClient:
    directory_client = file_system_client.get_directory_client(directory_name)

    if not directory_client.exists():
        directory_client = file_system_client.create_directory(directory_name)

    return directory_client

def auth_and_get_fs_dir_client(file_system_name: str, directory_name: str) -> DataLakeDirectoryClient:
    auth_client = get_service_client_token_credential()
    fs_client = get_or_make_file_system(auth_client, file_system_name)
    dir_client = get_or_make_directory(fs_client, directory_name)

    return dir_client

def auth_blob_client() -> BlobServiceClient:
    connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    blob_client = BlobServiceClient.from_connection_string(connect_str)

    return blob_client

def set_content_type(blob_client: BlobServiceClient, containter_name: str, dir_name:str, filename:str):
    blob_file = blob_client.get_blob_client(containter_name, os.path.join(dir_name, filename))

    if '.html' in filename:
        blob_file.set_http_headers(ContentSettings(content_type='text/html'))
    elif '.js' in filename:
        blob_file.set_http_headers(ContentSettings(content_type='text/javascript'))
    elif '.png' in filename:
        blob_file.set_http_headers(ContentSettings(content_type='image/png'))
    elif '.css' in filename:
        blob_file.set_http_headers(ContentSettings(content_type='text/css'))


# Azure location
containter_name = '$web'
dir_name = 'pytest-cov-report'

# Local location
html_dir = 'assets/htmlcov'

# Azure clients
fs_dir_client = auth_and_get_fs_dir_client(containter_name, dir_name)
blob_client = auth_blob_client()

# Copy each file over to Azure
for filename in os.listdir(html_dir):
    local_file = os.path.join(html_dir, filename)

    if os.path.isfile(local_file):
        with open(local_file, 'rb') as data:
            azure_file_client = fs_dir_client.get_file_client(filename)
            azure_file_client.upload_data(data, overwrite=True)

        set_content_type(blob_client, containter_name, dir_name, filename)

    else:
        print('Non file found!\n', filename)
        exit(1)