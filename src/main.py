import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.router import api_router
from core.config import app_settings

app = FastAPI(
    title=app_settings.app_title,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)
app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=app_settings.host,
        port=app_settings.port,
    )
