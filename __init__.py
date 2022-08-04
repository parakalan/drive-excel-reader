from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from utils import authenticate, get_file_id_from_url

import io

import pandas as pd


def read_excel(file_url, sheet_name=None):
    file_id = get_file_id_from_url(file_url)
    try:
        service = build('drive', 'v3', credentials=authenticate())
        try:
            request = service.files().get_media(fileId=file_id)
            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
        except:
            request = service.files().export_media(fileId=file_id,
                                                   mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
    except HttpError as error:
        print(F'An error occurred: {error}')
        raise
    if sheet_name:
        return pd.read_excel(file.getvalue(), engine=None, sheet_name=sheet_name)
    else:
        return pd.read_excel(file.getvalue(), engine=None)
