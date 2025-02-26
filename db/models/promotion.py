from datetime import datetime
from uuid import uuid4
import re
from fastapi import HTTPException
from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import FileType
from sqlalchemy import Text, TIMESTAMP
from sqlalchemy.event import listens_for
from sqlalchemy.orm import Mapped, mapped_column

from api.dependencies.images import check_image
from config.config import settings
from db.connection import Base


class Promotion(Base):
    __tablename__ = "promotions"

    title: Mapped[str]
    title_uz: Mapped[str] = mapped_column(nullable=True)

    content: Mapped[str] = mapped_column(Text)
    content_uz: Mapped[str] = mapped_column(Text, nullable=True)

    image: Mapped[FileType] = mapped_column(
        FileType(storage=FileSystemStorage(path=settings.PROMOTION_URL)), nullable=True
    )
    image_url: Mapped[str] = mapped_column(default="")
    poster: Mapped[FileType] = mapped_column(
        FileType(storage=FileSystemStorage(path=settings.PROMOTION_URL)), nullable=True
    )
    poster_url: Mapped[str] = mapped_column(default="")
    start_date: Mapped[datetime] = mapped_column()
    end_date: Mapped[datetime] = mapped_column()
    position: Mapped[int] = mapped_column(nullable=True)



@listens_for(Promotion, "before_update")
def before_update_listener(mapper, connection, target):

    if target.start_date > target.end_date:
        raise HTTPException(
            status_code=400, detail="Конечная дата должна быть позже начальной"
        )
    try:
        check_image(target.image)
        check_image(target.poster)
    except AttributeError as e:
        pass
    filename = f"{uuid4().hex}{target.image.filename.replace(" ", "")}"
    filename = re.sub(r'[А-Яа-яЁё]', '', filename)

    target.image.filename = filename
    target.image_url = f"{settings.PROMOTION_URL}{filename}"

    poster_name = f"{uuid4().hex}{target.poster.filename.replace(" ", "")}"
    poster_name = re.sub(r'[А-Яа-яЁё]', '', poster_name)

    target.poster.filename = poster_name
    target.poster_url = f"{settings.PROMOTION_URL}{poster_name}"


@listens_for(Promotion, "before_insert")
def before_insert_listener(mapper, connection, target):

    if target.start_date > target.end_date:
        raise HTTPException(
            status_code=400, detail="Конечная дата должна быть позже начальной"
        )

    try:
        check_image(target.image)
        check_image(target.poster)
    except AttributeError as e:
        pass

    filename = f"{uuid4().hex}{target.image.filename.replace(" ", "")}"
    filename = re.sub(r'[А-Яа-яЁё]', '', filename)

    target.image.filename = filename
    target.image_url = f"{settings.PROMOTION_URL}{filename}"

    poster_name = f"{uuid4().hex}{target.poster.filename.replace(" ", "")}"
    poster_name = re.sub(r'[А-Яа-яЁё]', '', poster_name)

    target.poster.filename = poster_name
    target.poster_url = f"{settings.PROMOTION_URL}{poster_name}"
