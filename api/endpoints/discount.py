from typing import List

from fastapi import APIRouter

from api.dependencies.dates import validate_dates
from db.repositories.discount import DiscountRepository
from db.schemas.discount import DiscountSchemaFull, DiscountSchema

router = APIRouter(
    prefix="/discount",
    tags=["Скидки"],
)


@router.get("/", response_model=List[DiscountSchemaFull])
async def get_all(
    page: int = 1,
    limit: int = 10,
):
    discounts = await DiscountRepository.get_all(page, limit)

    for discount in discounts:
        for product in discount.products:
            if discount.discount_type.name == "percent":
                product.price = round(
                    product.price - (product.price * discount.value / 100), 2
                )
            elif discount.discount_type.name == "fixed":
                product.price = round(product.price - discount.value, 2)

    return discounts


@router.get("/{id}")
async def get_discount(id: int):
    discount = await DiscountRepository.get_by_id(id)
    if not discount:
        return {}

    for product in discount.products:
        if discount.discount_type.name == "percent":
            product.price = round(
                product.price - (product.price * discount.value / 100), 2
            )
        elif discount.discount_type.name == "fixed":
            product.price = round(product.price - discount.value, 2)

    return discount if discount.is_active else {}


@router.post("/")
async def create_discount(discount: DiscountSchema):
    await validate_dates(discount.start_date, discount.end_date)

    result = await DiscountRepository.add_record(**discount.dict())

    return result
