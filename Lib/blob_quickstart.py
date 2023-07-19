from storage_utils import StorageUtil

if __name__ == '__main__':
    # Azure location
    containter_name = 'intern-blob-quickstart'
    azure_file = 'test.txt'

    # Local location
    local_file = 'assets/test.txt'

    # Azure client
    blob_client = StorageUtil.get_auth_blob_client()

    blob_container_client = StorageUtil.get_and_make_container_client(blob_client, containter_name) 

    with open(local_file, 'rb') as data:
        blob_container_client.upload_blob(name=azure_file, data=data, overwrite=True)

    StorageUtil.set_blob_content_type(blob_client, containter_name=containter_name, dir_name=None, filename=azure_file)
