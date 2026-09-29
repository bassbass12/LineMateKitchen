from fastapi import APIRouter, HTTPException
from app.models.ticket import Ticket

router = APIRouter(prefix="/tickets", tags=["Tickets"])
from app.data_loader import load_tickets

tickets = load_tickets()

@router.get("/", response_model=list[Ticket])
def get_tickets():
    return tickets

@router.post("/", response_model=Ticket)
def create_ticket(ticket: Ticket):
    tickets.append(ticket)
    return ticket


@router.get("/{ticket_id}", response_model=Ticket)
def get_ticket(ticket_id: int):
    for ticket in tickets:
        if ticket.id == ticket_id:
            return ticket

    raise HTTPException(status_code=404, detail="Ticket not found")

@router.delete("/{ticket_id}")
def delete_ticket(ticket_id: int):
    for ticket in tickets:
        if ticket.id == ticket_id:
            tickets.remove(ticket)
            return {"message": "Ticket deleted"}

    raise HTTPException(status_code=404, detail="Ticket not found")