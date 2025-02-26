import os
from datetime import date
from uuid import uuid4


from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import ImageType, FileType
from sqlalchemy import Text, func, TIMESTAMP
from sqlalchemy.event import listens_for
from sqlalchemy.orm import Mapped, mapped_column
import re
from api.dependencies.images import check_image
from api.services.images import save_image
from config.config import settings
from db.connection import Base


class News(Base):
    __tablename__ = "news"

    title: Mapped[str]
    title_uz: Mapped[str] = mapped_column(nullable=True)

    content: Mapped[str] = mapped_column(Text)
    content_uz: Mapped[str] = mapped_column(Text, nullable=True)

    image: Mapped[FileType] = mapped_column(
        FileType(storage=FileSystemStorage(path=settings.NEWS_URL)), nullable=True
    )
    image_url: Mapped[str] = mapped_column(default="")
    created_at: Mapped[date] = mapped_column(server_default=func.now())

    is_active: Mapped[bool] = mapped_column(default=True)


@listens_for(News, "before_update")
def before_update_listener(mapper, connection, target):
    try:
        check_image(target.image)
    except AttributeError as e:
        pass

    filename = f"{uuid4().hex}{target.image.filename.replace(' ', '')}"
    filename = re.sub(r'[А-Яа-яЁё]', '', filename)

    target.image.filename = filename
    target.image_url = f"{settings.NEWS_URL}{filename}"


@listens_for(News, "before_insert")
def before_insert_listener(mapper, connection, target):
    check_image(target.image)
    filename = f"{uuid4().hex}{target.image.filename.replace(' ', '')}"
    filename = re.sub(r'[А-Яа-яЁё]', '', filename)

    target.image.filename = filename.replace(" ", "")
    target.image_url = f"{settings.NEWS_URL}{filename}"


