import os
from storage_utils import StorageUtil

if __name__ == '__main__':
    # Azure location
    containter_name = '$web'
    dir_name = 'pytest-cov-report'

    # Local location
    html_dir = 'assets/htmlcov'

    # Azure clients
    fs_dir_client = StorageUtil.get_auth_datalake_client(containter_name, dir_name)
    blob_client = StorageUtil.get_auth_blob_client()

    # Copy each file over to Azure
    for filename in os.listdir(html_dir):
        local_file = os.path.join(html_dir, filename)

        if os.path.isfile(local_file):
            with open(local_file, 'rb') as data:
                azure_file_client = fs_dir_client.get_file_client(filename)
                azure_file_client.upload_data(data, overwrite=True)

            StorageUtil.set_blob_content_type(blob_client, containter_name, dir_name, filename)

        else:
            print('Non file found!\n', filename)
            exit(1)