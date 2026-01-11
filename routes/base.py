from fastapi import Depends, FastAPI, APIRouter
import os
from helpers.config import get_settings,Settings
base_router = APIRouter(prefix="/api/v1",
                         tags=["/api/v1"])

@base_router.get("/")
async def welcome(app_settings: Settings = Depends(get_settings)):
#async def welcome():
    #app_settings = get_settings() #why when i use Depends it gives error?
    app_name = app_settings.APP_NAME
    app_version = app_settings.APP_VERSION
    return {"App Name": app_name, "App Version": app_version}