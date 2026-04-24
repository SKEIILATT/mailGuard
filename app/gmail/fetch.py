import time


def fetch_all_message_ids(service):
    LABELS = [
        'INBOX',
        'SPAM',
        'CATEGORY_PROMOTIONS',
        'CATEGORY_SOCIAL',
        'CATEGORY_UPDATES'
    ]

    all_ids = set()

    for label in LABELS:
        print(f"Obteniendo correos de {label}...")
        page_token = None

        while True:
            params = {
                'userId': 'me',
                'labelIds': [label]
            }
            if page_token:
                params['pageToken'] = page_token

            results = service.users().messages().list(**params).execute()
            messages = results.get('messages', [])
            all_ids.update([m['id'] for m in messages])

            print(f"   {len(all_ids)} IDs unicos acumulados...", end='\r')

            page_token = results.get('nextPageToken')
            if not page_token:
                break

    print(f"\nTotal: {len(all_ids)} correos unicos encontrados")
    return list(all_ids)


def fetch_emails_batch(service, ids):
    emails = []
    chunks = [ids[i:i+100] for i in range(0, len(ids), 100)]

    print(f"Obteniendo detalles en {len(chunks)} lotes...\n")

    for i, chunk in enumerate(chunks):
        print(f"   Procesando lote {i+1}/{len(chunks)}...", end='\r')

        results = []

        def make_callback(msg_id):
            def callback(request_id, response, exception):
                if exception:
                    return
                headers = response['payload']['headers']
                subject = next(
                    (h['value'] for h in headers if h['name'] == 'Subject'),
                    '(sin asunto)'
                )
                sender = next(
                    (h['value'] for h in headers if h['name'] == 'From'),
                    '(desconocido)'
                )
                results.append({
                    'id': msg_id,
                    'subject': subject,
                    'from': sender
                })
            return callback

        batch = service.new_batch_http_request()

        for msg_id in chunk:
            batch.add(
                service.users().messages().get(
                    userId='me',
                    id=msg_id,
                    format='metadata',
                    metadataHeaders=['From', 'Subject']
                ),
                callback=make_callback(msg_id)
            )

        batch.execute()
        emails.extend(results)
        time.sleep(0.5)

    print(f"\nDetalles obtenidos de {len(emails)} correos")
    return emails

def get_senders(emails):
    senders = {}

    for email in emails:
        sender = email['from']
        email_id = email['id']

        if sender in senders:
            senders[sender]['count'] += 1
            senders[sender]['ids'].append(email_id)
        else:
            senders[sender] = {
                'sender': sender,
                'count': 1,
                'ids': [email_id],
                'example_subject': email['subject']
            }

    return sorted(senders.values(), key=lambda x: x['count'], reverse=True)
