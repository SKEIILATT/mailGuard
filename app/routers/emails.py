from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from googleapiclient.discovery import build
from app.gmail.auth import authenticate
from app.gmail.fetch import fetch_all_message_ids, fetch_emails_batch, get_senders
from app.gmail.actions import process_senders

router = APIRouter()

class ProcessRequest(BaseModel):
    selected_senders: List[str]
    action: str

@router.get('/senders')
def get_all_senders():
    creds = authenticate()
    service = build('gmail', 'v1', credentials=creds)

    ids = fetch_all_message_ids(service)
    emails = fetch_emails_batch(service, ids)
    senders = get_senders(emails)

    return {
        'total_senders': len(senders),
        'senders': [
            {
                'sender': s['sender'],
                'count': s['count'],
                'example_subject': s['example_subject']
            }
            for s in senders
        ]
    }

@router.post('/process')
def process(request: ProcessRequest):
    creds = authenticate()
    service = build('gmail', 'v1', credentials=creds)

    ids = fetch_all_message_ids(service)
    emails = fetch_emails_batch(service, ids)
    senders = get_senders(emails)

    result = process_senders(
        service,
        senders,
        request.selected_senders,
        request.action
    )

    return result