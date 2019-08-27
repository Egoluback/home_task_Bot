# Constants

from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
from googleapiclient.discovery import build
import pprint
import io

pp = pprint.PrettyPrinter(indent=4)

TOKEN = 'b4ee4a01ecf6ae3e405fc8903e3ae97436e894193fc25ce8335ba1f5bac032c76bad75adb176f15f793e4'
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'api/service-key.json'
PUBLIC_ID = 185880701