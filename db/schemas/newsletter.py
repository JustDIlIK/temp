from pydantic import BaseModel, EmailStr


class NewsletterSchema(BaseModel):
    email: EmailStr


class NewsletterSchemaFull(NewsletterSchema):
    id: int
