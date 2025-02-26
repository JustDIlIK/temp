from datetime import datetime

from pydantic import BaseModel


class PromotionSchema(BaseModel):
    title: str
    content: str
    title_uz: str
    content_uz: str
    image_url: str
    poster_url: str
    start_date: datetime = "2025-01-31T17:37:56"
    end_date: datetime = "2025-03-31T17:37:56"


class PromotionSchemaFull(PromotionSchema):
    id: int
