from pydantic import BaseModel


class VacancySchema(BaseModel):
    title: str
    description: str
    address: str
    title_uz: str
    description_uz: str
    address_uz: str



class VacancySchemaFull(VacancySchema):
    id: int
