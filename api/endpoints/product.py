import asyncio
import os
from idlelib.query import Query
from typing import List, Optional
from uuid import uuid4

from fastapi import APIRouter, UploadFile, Body, Form, File, HTTPException, Depends

from api.dependencies.images import check_image
from api.services.images import save_image
from config.config import settings
from db.repositories.product import ProductRepository
from db.schemas.product import ProductSchema, ProductSchemaFull

router = APIRouter(
    prefix="/products",
    tags=["Продукты"],
)

@router.get("/", response_model=List[ProductSchemaFull])
async def get_products(
    page: int = 1,
    limit: int = 10,
):

    products = await ProductRepository.get_all(page, limit)
    #
    # if products and len(products) > 0 and local == "UZ":
    #     for product in products:
    #         product.title = product.title_uz
    #         product.description = product.description_uz


    ### Deprecated ###
    # for product in products:
    #     if product.discount:
    #         discount = product.discount
    #         if discount.discount_type.name == "percent":
    #             product.price = round(
    #                 product.price - (product.price * discount.value / 100), 2
    #             )
    #         elif discount.discount_type.name == "fixed":
    #             product.price = round(product.price - discount.value, 2)

    return products


@router.get("/{id}", response_model=ProductSchemaFull)
async def get_product(id: int):
    product = await ProductRepository.get_by_id(id)

    if (not product is None and (not product.is_available or product.new_price is None)) or product is None:
        raise HTTPException(status_code=404, detail="Продукт не найден")

    return product if product.is_available else {}



@router.post("/")
async def create_product(
    file: UploadFile = Depends(check_image),
    title: str = Body(...),
    description: str = Body(...),
    price: int = Body(...),
    is_available: bool = Body(...),
    category_id: int = Body(...),
    discount_id: Optional[int] = Body(None),
):
    file_path = await save_image(file, settings.PRODUCT_URL)

    result = await ProductRepository.add_record(
        title=title,
        description=description,
        price=price,
        is_available=is_available,
        image=file,
        image_url=file_path,
        category_id=category_id,
        discount_id=discount_id,
    )
    return result


@router.post("/search")
async def search_product(query: str):
    await asyncio.sleep(0.3)

    result = await ProductRepository.find_all(title=query, description=query)

    return result
