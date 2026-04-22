from googleapiclient.discovery import build


def delete_emails(service, ids):
    chunks = [ids[i : i + 100] for i in range(0, len(ids), 100)]
    total_deleted = 0

    print(f"Eliminando {len(ids)} correos en {len(chunks)} lotes...")

    for i, chunk in enumerate(chunks):
        print(f"   Procesando lote {i + 1}/{len(chunks)}...", end="\r")
        service.users().messages().batchDelete(
            userId="me", body={"ids": chunk}
        ).execute()
        total_deleted += len(chunk)

    print(f"\nEliminados {total_deleted} correos")


def archive_emails(service, ids):
    chunks = [ids[i : i + 100] for i in range(0, len(ids), 100)]
    total_archived = 0

    print(f"Archivando {len(ids)} correos en {len(chunks)} lotes...")

    for i, chunk in enumerate(chunks):
        print(f"   Procesando lote {i + 1}/{len(chunks)}...", end="\r")
        service.users().messages().batchModify(
            userId="me", body={"ids": chunk, "removeLabelIds": ["INBOX"]}
        ).execute()
        total_archived += len(chunk)

    print(f"\nArchivados {total_archived} correos")


def process_senders(service, senders, selected_senders, action):
    ids_to_process = []

    for s in senders:
        if s["sender"] in selected_senders:
            ids_to_process.extend(s["ids"])

    if not ids_to_process:
        print("No se encontraron correos para procesar")
        return

    print(
        f"\n{len(ids_to_process)} correos encontrados de {len(selected_senders)} remitentes"
    )

    if action == "delete":
        delete_emails(service, ids_to_process)
    elif action == "archive":
        archive_emails(service, ids_to_process)
    else:
        print(f"Accion desconocida: {action}")
