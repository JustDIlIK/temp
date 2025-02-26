from datetime import time

from pydantic import BaseModel


class ShopSchema(BaseModel):
    title: str
    address: str
    landmark: str
    title_uz: str
    address_uz: str
    landmark_uz: str
    open_at: time
    close_at: time
    longitude: float
    latitude: float



class ShopSchemaFull(ShopSchema):
    id: int
