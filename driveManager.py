# Drive Manager class

from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
from googleapiclient.discovery import build
from const import *

import pprint
import io

class DriveManager:
    def __init__(self, pathLocal, folderId, fileId = ''):
        self.fileId = fileId
        self.pathLocal = pathLocal
        self.folderId = folderId

        self.credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        self.service = build('drive', 'v3', credentials = self.credentials)
    
    def setFileId(self, fileId):
        self.fileId = fileId

    def findFile(self):
        files = self.service.files().list(
            pageSize=5, 
            fields="nextPageToken, files(id, name, mimeType, parents, createdTime)",
            q="'" + self.folderId + "' in parents").execute()

        try:
            for file in files['files']:
                pp.pprint("File id - " + file['name'])
                if (file['name'] == "dataFile.json"):
                    return file['id']
        except:
            print("There is new http error")

    def deleteAll(self):
        files = self.service.files().list(
            pageSize=5, 
            fields="nextPageToken, files(id, name, mimeType, parents, createdTime)",
            q="'" + self.folderId + "' in parents").execute()

        try:
            for file in files['files']:
                pp.pprint("File id - " + file['name'])
                if (file['name'] == "dataFile.json"):
                    self.service.files().delete(fileId = file['id']).execute()
                    print('Successfully deleted.')
        except:
            print("There is new http error")


    def download(self):
        if (self.fileId == '' or self.fileId == None):
            return
        print(self.fileId)
        request = self.service.files().get_media(fileId = self.fileId)
        fh = io.FileIO(self.pathLocal, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print ("Download %d%%." % int(status.progress() * 100))
    
    def load(self):
        self.deleteAll()

        name = 'dataFile.json'
        fileMetadata = {
            'name': name,
            'parents': [
                    self.folderId
                ]
        }
        media = MediaFileUpload(self.pathLocal, resumable = True)
        fileInfo = self.service.files().create(body = fileMetadata, media_body = media, fields = 'id').execute()
        self.fileId = fileInfo['id']
        pp.pprint("New file id - " + fileInfo['id'])
