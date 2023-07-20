from storage_utils import StorageUtil

if __name__ == '__main__':
    # Azure location
    containter_name = 'intern-blob-quickstart'
    azure_file = 'test.txt'

    # Local location
    local_file = 'assets/test.txt'

    # Azure client
    storage_util = StorageUtil()
    blob_client = storage_util.get_auth_blob_client()

    blob_container_client = storage_util.get_and_make_container_client(blob_client, containter_name) 

    with open(local_file, 'rb') as data:
        blob_container_client.upload_blob(name=azure_file, data=data, overwrite=True)

    storage_util.set_blob_content_type(blob_client, containter_name=containter_name, dir_name=None, filename=azure_file)

    print(f"Uploaded {local_file} to the {containter_name} container:")
    print(f"\tName: {next(blob_container_client.list_blobs(name_starts_with=azure_file))['name']}")
    print(f"\tLast Updated: {next(blob_container_client.list_blobs(name_starts_with=azure_file))['last_modified']}")
