from fastapi import APIRouter
import pandas as pd
import numpy as np

from datetime import datetime, timedelta

router = APIRouter(prefix="/analytics", tags=["Analytics"])

CREW_STATIONS = {
    10: "Grill",
    11: "Pastry",
    12: "Prep",
    13: "Front of House"
}


@router.get("/tickets")
def ticket_workload():
    from app.routers.tickets import tickets

    if not tickets:
        return {"message": "No tickets available"}

    data = [ticket.model_dump() for ticket in tickets]
    df = pd.DataFrame(data)

    df["station"] = df["assignee_id"].map(CREW_STATIONS)

    workload = (
        df.groupby(["station", "priority"])
        .size()
        .reset_index(name="count")
    )

    open_tickets = df[df["status"] == "Open"]
    station_counts = open_tickets.groupby("station").size()

    station_counts = station_counts.reindex(
        CREW_STATIONS.values(),
        fill_value=0
    )

    average_open_tickets = float(np.mean(station_counts.values))

    disproportionate_stations = [
        {
            "station": station,
            "open_ticket_count": int(count)
        }
        for station, count in station_counts.items()
        if count > average_open_tickets
    ]

    return {
        "workload": workload.to_dict(orient="records"),
        "average_open_tickets_per_station": average_open_tickets,
        "disproportionate_stations": disproportionate_stations
    }


@router.get("/ownership-mismatch")
def ownership_mismatch():
    from app.routers.tickets import tickets
    from app.routers.documents import documents

    mismatches = []

    for ticket in tickets:
        if ticket.status != "Open":
            continue

        if ticket.assignee_id is None or ticket.related_document_id is None:
            continue

        document = next(
            (doc for doc in documents if doc.id == ticket.related_document_id),
            None
        )

        if document is None:
            continue

        assignee_station = CREW_STATIONS.get(ticket.assignee_id)
        owner_station = CREW_STATIONS.get(document.owner_id)

        if assignee_station != owner_station:
            mismatches.append({
                "ticket_id": ticket.id,
                "ticket_title": ticket.title,
                "assignee_station": assignee_station,
                "document_title": document.title,
                "owner_station": owner_station
            })

    return mismatches


@router.get("/stale-documents")
def stale_documents():
    from app.routers.documents import documents

    cutoff = datetime.now() - timedelta(days=90)

    stale = []

    for document in documents:
        if document.category != "Incident Report":
            if (
                document.last_reviewed_at is None
                or document.last_reviewed_at < cutoff
            ):
                stale.append(document)

    return stale


@router.get("/triage")
def triage():
    from app.routers.tickets import tickets

    priority_order = {
        "Critical": 1,
        "High": 2,
        "Medium": 3,
        "Low": 4
    }

    open_tickets = [
        ticket for ticket in tickets
        if ticket.status == "Open"
    ]

    open_tickets.sort(
        key=lambda ticket: priority_order.get(ticket.priority, 99)
    )

    return open_tickets