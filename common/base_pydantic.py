"""
自定义的pydantic.BaseModel
"""
from datetime import date, datetime

from pydantic import BaseModel

from conf.settings import settings


class CreatorOut(BaseModel):
    id: int
    name: str
    username: str


class CustomBaseModel(BaseModel):
    class Config:
        json_encoders = {
            datetime: lambda dt: dt.strftime(settings.DATETIME_FORMAT),
            date: lambda dt: dt.strftime(settings.DATE_FORMAT),
        }
