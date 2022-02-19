import sys
from google.auth import compute_engine
import base64
import email
# variables

# environment variables
creds='/opt/web/contactus/keys/get.json'

# API variables

username = sys.argv[1].lower()

# list scopes required using credentials


SCOPES = ['https://mail.google.com/','https://mail.google.com/','https://www.googleapis.com/auth/gmail.modify','https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.metadata']

SERVICE_ACCOUNT_FILE = creds
service_account_info = json.load(open('/opt/web/contactus/keys/get.json'))
credentials = service_account.Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
delegated_credentials = credentials.with_subject(username)
service = googleapiclient.discovery.build('gmail', 'v1', credentials=delegated_credentials)

# messages from inbox

def messages():
    try:
        response = service.users().messages().list(userId=username).execute()
        print(json.dumps(response))
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])
        for x in range(0,100):
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=username, pageToken=page_token,maxResults='1000').execute()
            print(json.dumps(response))
    except Exception as e:
        if hasattr(e,'message'):
            print(e.message)
        else:
            print(e)


messages()