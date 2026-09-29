from fastapi import APIRouter
import pandas as pd

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/tickets")
def ticket_workload():
    from app.routers.tickets import tickets

    if not tickets:
        return {"message": "No tickets available"}

    data = [ticket.model_dump() for ticket in tickets]
    df = pd.DataFrame(data)

    workload = (
        df.groupby(["priority", "status"])
        .size()
        .reset_index(name="count")
    )

    return workload.to_dict(orient="records")
