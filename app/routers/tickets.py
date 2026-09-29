from fastapi import APIRouter
from app.models.ticket import Ticket

router = APIRouter(prefix="/tickets", tags=["Tickets"])

tickets = []

@router.get("/", response_model=list[Ticket])
def get_tickets():
    return tickets

@router.post("/", response_model=Ticket)
def create_ticket(ticket: Ticket):
    tickets.append(ticket)
    return ticket
