from typing import List

from fastapi import APIRouter

from db.repositories.category import CategoryRepository
from db.schemas.category import CategorySchema, CategorySchemaFull

router = APIRouter(
    prefix="/category",
    tags=["Категории"],
)


@router.get("/")
async def get_all():
    result = await CategoryRepository.get_all()

    return result


@router.post("/")
async def create_category(category: CategorySchema):
    result = await CategoryRepository.add_record(**category.dict())
    return result
