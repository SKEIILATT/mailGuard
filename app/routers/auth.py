from fastapi import APIRouter
from googleapiclient.discovery import build
from app.gmail.auth import authenticate

router = APIRouter()

@router.get('/connect')
def connect():
    creds = authenticate()
    service = build('gmail', 'v1', credentials=creds)
    profile = service.users().getProfile(userId='me').execute()

    return {
        'status': 'connected',
        'email': profile['emailAddress'],
        'total_messages': profile['messagesTotal']
    }
