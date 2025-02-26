from pydantic import BaseModel


class ProductSchema(BaseModel):
    title: str
    description: str
    title_uz: str
    description_uz: str

    price: float
    new_price: float | None = None
    is_available: bool



class ProductSchemaFull(ProductSchema):
    id: int
    image_url: str
