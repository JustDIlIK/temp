from uuid import uuid4

from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import FileType
from sqlalchemy.event import listens_for
from sqlalchemy.orm import Mapped, mapped_column

from api.dependencies.images import check_image
from config.config import settings
from db.connection import Base
import re

class Social(Base):
    __tablename__ = "socials"

    title: Mapped[str]
    title_uz: Mapped[str] = mapped_column(nullable=True)

    url: Mapped[str]

    image: Mapped[FileType] = mapped_column(
        FileType(storage=FileSystemStorage(path=settings.SOCIAL_URL)), nullable=True
    )
    image_url: Mapped[str] = mapped_column(default="")

    is_available: Mapped[bool]

@listens_for(Social, "before_update")
def before_update_listener(mapper, connection, target):
    try:
        check_image(target.image)
    except AttributeError as e:
        pass
    filename = f"{uuid4().hex}{target.image.filename.replace(" ", "")}"
    filename = re.sub(r'[А-Яа-яЁё]', '', filename)

    target.image.filename = filename
    target.image_url = f"{settings.SOCIAL_URL}{filename}"


@listens_for(Social, "before_insert")
def before_insert_listener(mapper, connection, target):
    check_image(target.image)
    filename = f"{uuid4().hex}{target.image.filename.replace(" ", "")}"
    filename = re.sub(r'[А-Яа-яЁё]', '', filename)

    target.image.filename = filename
    target.image_url = f"{settings.SOCIAL_URL}{filename}"

