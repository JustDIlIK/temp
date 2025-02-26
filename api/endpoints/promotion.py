from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, UploadFile, Depends, Body, File, Form, HTTPException
from starlette.responses import JSONResponse

from api.dependencies.dates import validate_dates
from api.dependencies.images import check_image
from api.services.images import save_image
from config.config import settings
from db.repositories.promotion import PromotionRepository
from db.schemas.promotion import PromotionSchemaFull

router = APIRouter(
    prefix="/promotion",
    tags=["Акции"],
)

@router.get("/", response_model=List[PromotionSchemaFull])
async def get_promotions(
    page: int = 1,
    limit: int = 10
):
    promotions = await PromotionRepository.get_all(page, limit)

    return promotions


@router.get("/{id}", response_model=PromotionSchemaFull)
async def get_promotion(id: int):
    promotion = await PromotionRepository.get_by_id(id)


    if promotion is None:
        raise HTTPException(status_code=404, detail="Акция не найдена")

    return promotion




@router.post("/")
async def create_promotion(
    file: UploadFile = Depends(check_image),
    poster: UploadFile = Depends(check_image),
    title: str = Body(...),
    content: str = Body(...),
    start_date: datetime = Body(...),
    end_date: datetime = Body(...),
):

    await validate_dates(start_date, end_date)

    file_path = await save_image(file, settings.PROMOTION_URL)
    poster_path = await save_image(poster, settings.PROMOTION_URL)

    result = await PromotionRepository.add_record(
        title=title,
        content=content,
        image=file,
        image_url=file_path,
        poster=poster,
        poster_url=poster_path,
        start_date=start_date,
        end_date=end_date,
    )
    return result



@router.post("/upload")
async def upload_file(upload: UploadFile = File(...), ckCsrfToken: str = Form(...)):
    file_path = await save_image(upload, settings.PROMOTION_URL)
    return JSONResponse(
        content={
            "url": f"https://api-baraka.ai-softdev.com/{file_path}",
            "uploaded": True,
            "fileName": f"{file_path.split("/")[-1]}",
        }
    )
