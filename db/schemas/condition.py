from pydantic import BaseModel

class ConditionSchema(BaseModel):
    title: str
    title_uz: str
    position: int

class ConditionSchemaFull(ConditionSchema):
    id: int
