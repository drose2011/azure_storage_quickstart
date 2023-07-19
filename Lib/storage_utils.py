import os

from azure.storage.queue import QueueClient
from azure.core.exceptions import ResourceExistsError
from azure.storage.filedatalake import DataLakeServiceClient, DataLakeDirectoryClient, FileSystemClient
from azure.storage.blob import BlobServiceClient, ContentSettings

class StorageUtil:

    def __init__(self) -> None:
        self.connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        
    def get_and_make_auth_queue_client(self, queue_name: str) -> QueueClient:
        queue_client = QueueClient.from_connection_string(conn_str=self.connect_str, queue_name=queue_name)
        try:
            queue_client.create_queue()
        except ResourceExistsError:
            pass

        return queue_client

    def get_auth_blob_client(self) -> BlobServiceClient:
        blob_client = BlobServiceClient.from_connection_string(self.connect_str)

        return blob_client

    def get_auth_datalake_client(self) -> DataLakeServiceClient:
        service_client = DataLakeServiceClient.from_connection_string(self.connect_str)

        return service_client

    @staticmethod
    def get_and_make_container_client(blob_client: BlobServiceClient, containter_name: str):
        blob_container_client = blob_client.get_container_client(container=containter_name)

        if not blob_container_client.exists():
            blob_container_client.create_container()

        return blob_container_client

    @staticmethod
    def get_and_make_file_system(service_client: DataLakeServiceClient, file_system_name: str) -> FileSystemClient:
        file_system_client = service_client.get_file_system_client(file_system=file_system_name)

        if not file_system_client.exists():
            file_system_client = service_client.create_file_system(file_system=file_system_name)

        return file_system_client

    @staticmethod
    def get_and_make_directory(file_system_client: FileSystemClient, directory_name: str) -> DataLakeDirectoryClient:
        directory_client = file_system_client.get_directory_client(directory_name)

        if not directory_client.exists():
            directory_client = file_system_client.create_directory(directory_name)

        return directory_client

    def get_and_make_auth_datalake_dir_client(self, file_system_name: str, directory_name: str) -> DataLakeDirectoryClient:
        auth_client = self.get_auth_datalake_client()
        fs_client = self.get_and_make_file_system(auth_client, file_system_name)
        dir_client = self.get_and_make_directory(fs_client, directory_name)

        return dir_client

    @staticmethod
    def set_blob_content_type(blob_client: BlobServiceClient, containter_name: str, dir_name:str, filename:str):
        blob_loc = os.path.join(dir_name, filename) if dir_name is not None else filename
        blob_file = blob_client.get_blob_client(containter_name, blob_loc)

        if '.html' in filename:
            blob_file.set_http_headers(ContentSettings(content_type='text/html'))
        elif '.js' in filename:
            blob_file.set_http_headers(ContentSettings(content_type='text/javascript'))
        elif '.png' in filename:
            blob_file.set_http_headers(ContentSettings(content_type='image/png'))
        elif '.css' in filename:
            blob_file.set_http_headers(ContentSettings(content_type='text/css'))
        elif '.txt' in filename:
            blob_file.set_http_headers(ContentSettings(content_type='text/plain'))