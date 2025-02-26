from pydantic import BaseModel


class SocialSchema(BaseModel):
    title: str
    title_uz: str
    url: str
    is_available: bool


class SocialSchemaFull(SocialSchema):
    id: int
    image_url: str
