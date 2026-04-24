import time

from app.gmail.retry import execute_with_retry

def delete_emails(service, ids):
    chunks = [ids[i:i+100] for i in range(0, len(ids), 100)]
    total_deleted = 0

    for i, chunk in enumerate(chunks):
        print(f"   Eliminando lote {i+1}/{len(chunks)}...", end='\r')
        execute_with_retry(
            lambda: service.users().messages().batchDelete(
                userId='me',
                body={'ids': chunk}
            ).execute(),
            description='Eliminacion de correos',
        )
        total_deleted += len(chunk)
        time.sleep(1)

    print(f"\nEliminados {total_deleted} correos")
    return total_deleted

def archive_emails(service, ids):
    chunks = [ids[i:i+100] for i in range(0, len(ids), 100)]
    total_archived = 0

    for i, chunk in enumerate(chunks):
        print(f"   Archivando lote {i+1}/{len(chunks)}...", end='\r')
        execute_with_retry(
            lambda: service.users().messages().batchModify(
                userId='me',
                body={
                    'ids': chunk,
                    'removeLabelIds': ['INBOX']
                }
            ).execute(),
            description='Archivado de correos',
        )
        total_archived += len(chunk)
        time.sleep(1)

    print(f"\nArchivados {total_archived} correos")
    return total_archived

def process_senders(service, senders, selected_senders, action):
    ids_to_process = []

    for s in senders:
        if s['sender'] in selected_senders:
            ids_to_process.extend(s['ids'])

    if not ids_to_process:
        return {
            'status': 'error',
            'message': 'No se encontraron correos para procesar'
        }

    if action == 'delete':
        total = delete_emails(service, ids_to_process)
    elif action == 'archive':
        total = archive_emails(service, ids_to_process)
    else:
        return {
            'status': 'error',
            'message': f'Accion desconocida: {action}'
        }

    return {
        'status': 'success',
        'action': action,
        'total': total,
        'senders': selected_senders
    }
