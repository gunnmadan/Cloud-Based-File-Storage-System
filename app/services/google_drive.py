from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
<<<<<<< HEAD
from google_auth_oauthlib.flow import InstalledAppFlow
=======
>>>>>>> miracle/main
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

class GoogleDriveService:
    def __init__(self, credentials_path):
        self.SCOPES = ['https://www.googleapis.com/auth/drive.file']
        self.credentials_path = credentials_path
        self.service = None
        self._init_service()

    def _init_service(self):
<<<<<<< HEAD
        flow = InstalledAppFlow.from_client_secrets_file(
            self.credentials_path, self.SCOPES
        )
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

=======
        creds = Credentials.from_authorized_user_file(self.credentials_path, self.SCOPES)
>>>>>>> miracle/main
        self.service = build('drive', 'v3', credentials=creds)

    def upload_file(self, file_content, filename, mime_type):
        try:
            file_metadata = {'name': filename}
            media = MediaIoBaseUpload(
                io.BytesIO(file_content),
                mimetype=mime_type,
                resumable=True
            )
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            return file.get('id')
        except Exception as e:
            raise Exception(f"Error uploading file: {str(e)}")

    def download_file(self, file_id):
        try:
            request = self.service.files().get_media(fileId=file_id)
            file_content = request.execute()
            return file_content
        except Exception as e:
            raise Exception(f"Error downloading file: {str(e)}")

    def create_share_link(self, file_id):
        try:
            permission = {
                'type': 'anyone',
                'role': 'reader'
            }
            self.service.permissions().create(
                fileId=file_id,
                body=permission
            ).execute()
            
            file = self.service.files().get(
                fileId=file_id,
                fields='webViewLink'
            ).execute()
            return file.get('webViewLink')
        except Exception as e:
            raise Exception(f"Error creating share link: {str(e)}")