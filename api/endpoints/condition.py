from typing import List

from fastapi import APIRouter

from db.repositories.condition import ConditionRepository
from db.schemas.condition import ConditionSchemaFull, ConditionSchema

router = APIRouter(
    prefix="/condition",
    tags=["Условия Работы"],
)


@router.get("/", response_model=List[ConditionSchemaFull])
async def get_all():

    result = await ConditionRepository.get_all()

    return result


@router.post("/")
async def create_condition(condition: ConditionSchema):
    result = await ConditionRepository.add_record(**condition.dict())
    return result
