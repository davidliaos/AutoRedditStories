import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

def upload_to_drive(filename):
    """Uploads the specified file to Google Drive.

    Args:
        filename (str): The name of the file to be uploaded.

    Returns:
        None
    """
    SCOPES = ["https://www.googleapis.com/auth/drive.file"]
    file_path = os.path.join("mp4", filename)

    try:
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        # build the Drive API client
        service = build("drive", "v3", credentials=creds)

        # create a MediaFileUpload object for the file
        file = MediaFileUpload(file_path, mimetype="video/mp4", resumable=True)

        # create a file resource with metadata
        file_metadata = {"name": filename, "parents": [folder_id]}

        # send a request to upload the file
        uploaded_file = (
            service.files()
            .create(body=file_metadata, media_body=file, fields="id")
            .execute()
        )

        print(
            f'File {filename} successfully uploaded to Google Drive ID:({uploaded_file.get("id")})'
        )

    except HttpError as error:
        print(f"An error occurred: {error}")
