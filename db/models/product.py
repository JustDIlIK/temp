from uuid import uuid4
import re
from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import FileType
from sqlalchemy import ForeignKey
from sqlalchemy.event import listens_for
from sqlalchemy.orm import Mapped, relationship, mapped_column

from api.dependencies.images import check_image
from config.config import settings
from db.connection import Base


class Product(Base):
    __tablename__ = "products"

    title: Mapped[str]
    title_uz: Mapped[str] = mapped_column(nullable=True)

    description: Mapped[str]
    description_uz: Mapped[str] = mapped_column(nullable=True)

    image: Mapped[FileType] = mapped_column(
        FileType(storage=FileSystemStorage(path=settings.PRODUCT_URL)), nullable=True
    )
    image_url: Mapped[str] = mapped_column(default="")

    price: Mapped[float]
    new_price: Mapped[float] = mapped_column(nullable=True)

    is_available: Mapped[bool]
		
    position: Mapped[int] = mapped_column(nullable=True)


    # category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    # discount_id: Mapped[int] = mapped_column(ForeignKey("discounts.id"), nullable=True)

    # discount = relationship("Discount", back_populates="products")
    # category = relationship("Category", back_populates="products")

    def __repr__(self):
        return f"Продукт - {self.title}"


@listens_for(Product, "before_update")
def before_update_listener(mapper, connection, target):
    try:
        check_image(target.image)

    except AttributeError as e:
        pass

    try:
        filename = f"{uuid4().hex}{target.image.filename.replace(' ', '')}"
        filename = re.sub(r'[А-Яа-яЁё]', '', filename)

        target.image.filename = filename
        target.image_url = f"{settings.PRODUCT_URL}{filename}"
    except AttributeError as e:
        pass


@listens_for(Product, "before_insert")
def before_insert_listener(mapper, connection, target):
    check_image(target.image)
    filename = f"{uuid4().hex}{target.image.filename.replace(' ', '')}"
    filename = re.sub(r'[А-Яа-яЁё]', '', filename)

    target.image.filename = filename
    target.image_url = f"{settings.PRODUCT_URL}{filename}"
