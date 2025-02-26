from datetime import date, datetime

from pydantic import BaseModel


class NewsSchema(BaseModel):
    title: str
    content: str
    title_uz: str
    content_uz: str
    image_url: str
    created_at: datetime


class NewsSchemaFull(NewsSchema):
    id: int
