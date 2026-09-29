from fastapi import FastAPI, Depends, Request

from app.routers.documents import router as documents_router
from app.routers.tickets import router as tickets_router
from app.routers.analytics import router as analytics_router
from app.routers.comments import router as comments_router


def get_app_name():
    return "LineMate Kitchen"


app = FastAPI(title="LineMate Kitchen")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"Request: {request.method} {request.url.path}")

    response = await call_next(request)

    print(f"Response: {response.status_code}")

    return response


app.include_router(documents_router)
app.include_router(tickets_router)
app.include_router(analytics_router)
app.include_router(comments_router)


@app.get("/")
def root(app_name: str = Depends(get_app_name)):
    return {"message": f"{app_name} API is running"}