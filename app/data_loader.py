import csv
from datetime import datetime

from app.models.document import Document
from app.models.ticket import Ticket
from app.models.comment import Comment


def load_documents():
    documents = []

    with open("data/documents.csv", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            documents.append(
                Document(
                    id=int(row["id"]),
                    title=row["title"],
                    category=row["category"],
                    body=row["body"],
                    owner_id=int(row["owner_id"]) if row["owner_id"] else None,
                    last_reviewed_at=(
                        datetime.fromisoformat(row["last_reviewed_at"])
                        if row["last_reviewed_at"]
                        else None
                    ),
                )
            )

    return documents


def load_tickets():
    tickets = []

    with open("data/tickets.csv", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            tickets.append(
                Ticket(
                    id=int(row["id"]),
                    title=row["title"],
                    priority=row["priority"],
                    status=row["status"],
                    assignee_id=int(row["assignee_id"]) if row["assignee_id"] else None,
                    related_document_id=(
                        int(row["related_document_id"])
                        if row["related_document_id"]
                        else None
                    ),
                    created_at=datetime.fromisoformat(row["created_at"]),
                )
            )

    return tickets

def load_comments():
    comments = []

    with open("data/comments.csv", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            comments.append(
                Comment(
                    id=int(row["id"]),
                    ticket_id=int(row["ticket_id"]),
                    author_id=int(row["author_id"]),
                    body=row["body"],
                    created_at=datetime.fromisoformat(row["created_at"]),
                )
            )

    return comments

def save_comments(comments):
    with open("data/comments.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "id",
            "ticket_id",
            "author_id",
            "body",
            "created_at"
        ])

        for comment in comments:
            writer.writerow([
                comment.id,
                comment.ticket_id,
                comment.author_id,
                comment.body,
                comment.created_at.isoformat()
            ])