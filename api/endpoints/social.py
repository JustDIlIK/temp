import os
from http.client import HTTPException
from typing import List
from uuid import uuid4

from fastapi import APIRouter, UploadFile, File, Body, Depends

from api.dependencies.images import check_image
from api.services.images import save_image
from config.config import settings
from db.models.socials import Social
from db.repositories.social import SocialRepository
from db.schemas.social import SocialSchemaFull

router = APIRouter(
    prefix="/social",
    tags=["Соц. сети"],
)


@router.get("/", response_model=List[SocialSchemaFull])
async def get_all():

    result = await SocialRepository.get_all()

    return result



@router.post("/")
async def create_social(
    file: UploadFile = Depends(check_image),
    title: str = Body(...),
    url: str = Body(...),
    is_available: bool = Body(...),
):

    file_path = await save_image(file, settings.SOCIAL_URL)

    result = await SocialRepository.add_record(
        title=title,
        url=url,
        is_available=is_available,
        image=file,
        image_url=file_path,
    )
    return result
