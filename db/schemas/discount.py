from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from db.schemas.product import ProductSchemaFull


class DiscountSchema(BaseModel):
    title: str
    discount_type: str
    value: float
    start_date: datetime = "2025-01-31T17:37:56"
    end_date: datetime = "2025-03-31T17:37:56"
    is_active: bool


class DiscountSchemaFull(DiscountSchema):
    id: int

    products: List[ProductSchemaFull]
