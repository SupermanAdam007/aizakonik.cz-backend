from logging.config import dictConfig
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.config import settings
from app.models import LogConfig

if settings.PROD:
    app = FastAPI(docs_url=None, redoc_url=None)
else:
    app = FastAPI()

print(f"Environment: {'Prod' if settings.PROD else 'Dev'}")

dictConfig(LogConfig().dict())
log = logging.getLogger("app")

from app.routers import predictions
from app.routers import constants

app.include_router(predictions.router)
app.include_router(constants.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
