import csv
from fetch_emails import authenticate, fetch_all_message_ids, fetch_emails_batch
from googleapiclient.discovery import build


def get_senders(emails):
    senders = {}

    for email in emails:
        sender = email["from"]
        email_id = email["id"]

        if sender in senders:
            senders[sender]["count"] += 1
            senders[sender]["ids"].append(email_id)
        else:
            senders[sender] = {
                "sender": sender,
                "count": 1,
                "ids": [email_id],
                "example_subject": email["subject"],
            }

    return sorted(senders.values(), key=lambda x: x["count"], reverse=True)


def export_to_csv(senders, filename="senders.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["sender", "count", "example_subject"])
        writer.writeheader()
        for s in senders:
            writer.writerow(
                {
                    "sender": s["sender"],
                    "count": s["count"],
                    "example_subject": s["example_subject"],
                }
            )
    print(f"Exportado a senders.csv")


def print_senders(senders):
    print(f"\n{len(senders)} remitentes unicos encontrados:\n")
    for i, s in enumerate(senders[:20]):
        print(f"  {i + 1:3}. [{s['count']:4} correos] {s['sender']}")
        print(f"        Ej: {s['example_subject'][:60]}")
    if len(senders) > 20:
        print(f"\n  ... y {len(senders) - 20} mas en senders.csv")


if __name__ == "__main__":
    creds = authenticate()
    service = build("gmail", "v1", credentials=creds)

    ids = fetch_all_message_ids(service)
    emails = fetch_emails_batch(service, ids)
    senders = get_senders(emails)

    print_senders(senders)
    export_to_csv(senders)

    print("\nAbre senders.csv para ver todos los remitentes")
