import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

#SCPOPE DE PERMISOS
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def authenticate():
    creds=None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json',SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def fetch_emails(service, max_results=20):
    results = service.users().messages().list(
        userId='me',
        maxResults=20,
        labelIds=['INBOX']
    ).execute()

    messages = results.get('messages', [])
    emails = []

    for msg in messages:
        detail = service.users().messages().get(
            userId='me',
            id=msg["id"],
            format='metadata',
            metadataHeaders=['From', 'Subject']
        ).execute()
        headers = detail['payload']['headers']
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(sin asunto)')
        sender  = next((h['value'] for h in headers if h['name'] == 'From'), '(desconocido)')

        emails.append({
            'id': msg['id'],
            'subject': subject,
            'from': sender
        })

    return emails

if __name__ == '__main__':
    creds = authenticate()
    service = build('gmail', 'v1', credentials=creds)
    emails = fetch_emails(service)

    print(f"\n Últimos {len(emails)} correos:\n")
    for email in emails:
        print(f"De:     {email['from']}")
        print(f"Asunto: {email['subject']}")
        print(f"ID:     {email['id']}")
        print("---")