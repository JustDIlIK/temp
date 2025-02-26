from typing import List

from fastapi import APIRouter

from db.repositories.newsletter import NewsletterRepository
from db.schemas.newsletter import NewsletterSchema

router = APIRouter(
    prefix="/newsletter",
    tags=["Подписка"],
)


@router.get("/")
async def get_all(
    page: int = 1,
    limit: int = 10,
):

    result = await NewsletterRepository.get_all(page, limit)

    return result



@router.post("/")
async def send_emails(email: NewsletterSchema):

    result = await NewsletterRepository.add_record(**email.dict())

    return result
