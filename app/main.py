from fastapi import FastAPI
from app.routers.documents import router as documents_router
from app.routers.tickets import router as tickets_router
from app.routers.analytics import router as analytics_router
from app.routers.comments import router as comments_router

app = FastAPI(title="LineMate Kitchen")

app.include_router(documents_router)
app.include_router(tickets_router)
app.include_router(analytics_router)
app.include_router(comments_router)

@app.get("/")
def root():
    return {"message": "LineMate Kitchen API is running"}
