from datetime import time

from fastapi import HTTPException
from sqlalchemy.event import listens_for
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from db.connection import Base


class Shop(Base):
    __tablename__ = "shops"

    title: Mapped[str]
    title_uz: Mapped[str] = mapped_column(nullable=True)

    address: Mapped[str]
    address_uz: Mapped[str] = mapped_column(nullable=True)

    landmark: Mapped[str]
    landmark_uz: Mapped[str] = mapped_column(nullable=True)

    open_at: Mapped[time]
    close_at: Mapped[time]

    longitude: Mapped[float]
    latitude: Mapped[float]


@listens_for(Shop, "before_update")
def before_update_listener(mapper, connection, target):
    if target.open_at > target.close_at:
        raise HTTPException(status_code=400, detail="Время закрытие должно быть позже")


@listens_for(Shop, "before_insert")
def before_insert_listener(mapper, connection, target):
    if target.open_at > target.close_at:
        raise HTTPException(status_code=400, detail="Время закрытие должно быть позже")
