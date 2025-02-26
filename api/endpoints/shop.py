from typing import List

from fastapi import APIRouter

from api.dependencies.dates import validate_time
from db.repositories.shop import ShopRepository
from db.schemas.shop import ShopSchemaFull, ShopSchema

router = APIRouter(
    prefix="/shop",
    tags=["Магазины"],
)

@router.get("/", response_model=List[ShopSchemaFull])
async def get_all():

    result = await ShopRepository.get_all()

    return result


@router.post("/")
async def create_shop(shop: ShopSchema):

    await validate_time(shop.open_at, shop.close_at)

    result = await ShopRepository.add_record(**shop.dict())

    return result
