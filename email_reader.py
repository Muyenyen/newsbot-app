import os
import re
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def fetch_news_links(service, query='subject:news OR subject:newsletter', max_results=10):
    results = service.users().messages().list(userId='me', q=query, maxResults=max_results).execute()
    messages = results.get('messages', [])
    links = []
    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
        parts = msg_data['payload'].get('parts', [])
        data = ''
        for part in parts:
            if part.get('mimeType') == 'text/plain':
                data = part['body'].get('data')
                break
        if not data:
            continue
        decoded_data = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
        found_links = re.findall(r'https?://\S+', decoded_data)
        links.extend(found_links)
    return links
