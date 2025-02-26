from typing import Optional, List

from pydantic import BaseModel


class CategorySchema(BaseModel):
    title: str
    description: str
    parent_id: Optional[int] = None


class CategorySchemaFull(CategorySchema):
    id: int
