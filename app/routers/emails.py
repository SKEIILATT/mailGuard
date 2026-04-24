from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from googleapiclient.discovery import build
from app.gmail.auth import authenticate
from app.gmail.cache import get_scan, save_scan
from app.gmail.fetch import fetch_all_message_ids, fetch_emails_batch, get_senders
from app.gmail.actions import process_senders

router = APIRouter()

class ProcessRequest(BaseModel):
    selected_senders: List[str]
    action: str
    scan_id: Optional[str] = None

@router.get('/senders')
def get_all_senders():
    creds = authenticate()
    service = build('gmail', 'v1', credentials=creds)

    ids = fetch_all_message_ids(service)
    emails = fetch_emails_batch(service, ids)
    senders = get_senders(emails)
    scan_id, expires_at = save_scan(senders)

    return {
        'scan_id': scan_id,
        'expires_at': expires_at,
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

    scan = get_scan(request.scan_id)
    if not scan:
        raise HTTPException(
            status_code=409,
            detail='No hay un escaneo vigente. Vuelve a consultar /emails/senders.'
        )

    result = process_senders(
        service,
        scan['senders'],
        request.selected_senders,
        request.action
    )

    return result
