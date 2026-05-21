from fastapi import FastAPI

from src.urls.v1 import api_router

from src.utils.exception_handlers import global_exception_handler


app = FastAPI(
    title="Blog Company Architecture API"
)


app.add_exception_handler(
    Exception,
    global_exception_handler
)


app.include_router(
    api_router,
    prefix="/api/v1"
)


@app.get("/")
async def home():
    return {
        "message": "Backend Running Successfully"
    }