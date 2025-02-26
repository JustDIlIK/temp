from typing import List

from fastapi import APIRouter, UploadFile, Depends, Body, File, Form, HTTPException
from starlette.datastructures import Headers
from starlette.responses import JSONResponse

from api.dependencies.images import check_image
from api.services.images import save_image
from config.config import settings
from db.repositories.news import NewsRepository
from db.schemas.news import NewsSchemaFull, NewsSchema

router = APIRouter(
    prefix="/news",
    tags=["Новости"],
)


@router.get("/", response_model=List[NewsSchemaFull])
async def get_all(
    page: int = 1,
    limit: int = 10
):
    result = await NewsRepository.get_all(page, limit)


    return result


@router.get("/{id}", response_model=NewsSchemaFull)
async def create_news(id: int):
    result = await NewsRepository.get_by_id(id)
    if (not result is None and not result.is_active) or result is None:
        raise HTTPException(status_code=404, detail="Новость не найдена")

    return result



@router.post("/")
async def create_news(
    file: UploadFile = Depends(check_image),
    title: str = Body(...),
    content: str = Body(...),
):
    file_path = await save_image(file, settings.NEWS_URL)
    file.headers = Headers(
        {
            "content-disposition": 'form-data; name="image"; filename="2.png"',
            "content-type": "image/png",
        }
    )
    result = await NewsRepository.add_record(
        title=title,
        content=content,
        image=file,
        image_url=file_path,
    )
    return result


@router.post("/upload")
async def upload_file(upload: UploadFile = File(...), ckCsrfToken: str = Form(...)):
    file_path = await save_image(upload, settings.NEWS_URL)
    return JSONResponse(
        content={
            "url": f"https://api-baraka.ai-softdev.com/{file_path}",
            "uploaded": True,
            "fileName": f"{file_path.split("/")[-1]}",
        }
    )
