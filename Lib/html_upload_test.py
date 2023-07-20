import os
from storage_utils import StorageUtil

if __name__ == '__main__':
    # Azure location
    containter_name = '$web'
    dir_name = 'pytest-cov-report'

    # Local location
    html_dir = 'assets/htmlcov'

    # Azure clients
    storage_util = StorageUtil()
    fs_dir_client = storage_util.get_and_make_auth_datalake_dir_client(containter_name, dir_name)
    blob_client = storage_util.get_auth_blob_client()

    # Copy each file over to Azure
    uploaded_files = []
    print("Starting upload of files:")
    for filename in os.listdir(html_dir):
        local_file = os.path.join(html_dir, filename)

        if os.path.isfile(local_file):
            with open(local_file, 'rb') as data:
                print(f"\tUploadeding {filename}")
                uploaded_files.append(filename)
                azure_file_client = fs_dir_client.get_file_client(filename)
                azure_file_client.upload_data(data, overwrite=True)

            storage_util.set_blob_content_type(blob_client, containter_name, dir_name, filename)

        else:
            print('Non file found!\n', filename)
            exit(1)
    
    print(f"Uploaded {len(uploaded_files)} files")