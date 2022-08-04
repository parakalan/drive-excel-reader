import os

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly',
          'https://www.googleapis.com/auth/drive.file',
          'https://www.googleapis.com/auth/drive.readonly']


def authenticate():
    creds = None
    token_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'token.json')

    if os.path.exists(os.path.join(token_path)):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    elif creds is None:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=49813)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def get_file_id_from_url(url):
    splits = url.split("/")
    idx = splits.index("d")
    return splits[idx + 1]

