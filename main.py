from googleapiclient.discovery import build
from fetch_emails import authenticate, fetch_all_message_ids, fetch_emails_batch
from senders import get_senders, export_to_csv
from actions import process_senders


def main():
    print("Iniciando MailGuard...\n")

    creds = authenticate()
    service = build("gmail", "v1", credentials=creds)

    ids = fetch_all_message_ids(service)
    emails = fetch_emails_batch(service, ids)
    senders = get_senders(emails)

    export_to_csv(senders)

    print(f"\n{len(senders)} remitentes unicos encontrados")
    print("Revisa senders.csv para ver la lista completa\n")

    return service, senders


if __name__ == "__main__":
    main()
