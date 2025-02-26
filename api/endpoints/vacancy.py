from typing import List

from fastapi import APIRouter

from db.repositories.vacancy import VacancyRepository
from db.schemas.vacancy import VacancySchemaFull, VacancySchema

router = APIRouter(
    prefix="/vacancies",
    tags=["Вакансии"],
)

@router.get("/", response_model=List[VacancySchemaFull])
async def get_all():
    result = await VacancyRepository.get_all()

    return result


@router.post("/")
async def create_discount(discount: VacancySchema):
    result = await VacancyRepository.add_record(**discount.dict())

    return result
