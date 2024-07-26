import os
import time

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Define your credentials and service account file
SERVICE_ACCOUNT_FILE = 'aiswtech-auto-bot.json'  # Path to your service account key file
SCOPES = ['https://www.googleapis.com/auth/drive.file']


# Create a service object
def create_service(api_name, api_version, scopes, key_file_location):
    credentials = service_account.Credentials.from_service_account_file(
        key_file_location, scopes=scopes
    )
    service = build(api_name, api_version, credentials=credentials)

    return service


def google_drive_run():
    service = create_service('drive', 'v3', SCOPES, SERVICE_ACCOUNT_FILE)
    return service


def google_drive_connect(folder_id, file_name, service):
    # folder_metadata = {
    #     'name': 'Rustamov Akobir',  # Name of the new folder
    #     'mimeType': 'application/vnd.google-apps.folder',
    #     'parents': ['16BSN3g_iElyOjQahoK6fLNB6490a0ZkQ']  # Parent folder ID
    # }
    #
    # # Create the new folder inside the specified parent folder
    # folder = service.files().create(body=folder_metadata, fields='id').execute()
    #
    # print(f'Folder ID: {folder.get("id")}')
    # print(f'Folder "New Subfolder" has been created inside the folder with ID: 16BSN3g_iElyOjQahoK6fLNB6490a0ZkQ')
    # FOLDER_ID = f'{folder.get("id")}'  # ID of the folder where the file will be uploaded

    FOLDER_ID = f'{folder_id}'  # ID of the folder where the file will be uploaded
    # folder_path = 'C:\\Users\\Ali\\my_project\\crypto_pay_system\\Med'

    FILE_TO_UPLOAD = f'Media/{file_name}'  # Path to the .pdf file you want to upload
    FILE_NAME = f'{file_name}'  # The name you want the file to have in Google Drive

    file_metadata = {
        'name': FILE_NAME,
        'parents': [FOLDER_ID]  # Specify the folder ID where you want to upload the file
    }

    media = MediaFileUpload(FILE_TO_UPLOAD, mimetype='application/pdf')

    file_drive = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    print(f'File "{FILE_TO_UPLOAD}" has been uploaded to Google Drive folder with ID: {FOLDER_ID}')
    time.sleep(0.01)


def delete_file(file_name):
    file_path = f'Media/{file_name}'
    try:
        os.remove(file_path)
        # print(f"File '{file_path}' has been deleted successfully.")
    except Exception as e:
        print(f"Error occurred while deleting the file: {e}")
