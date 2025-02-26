from datetime import datetime
from enum import Enum

from fastapi import HTTPException
from sqlalchemy import ForeignKey, TIMESTAMP
from sqlalchemy.event import listens_for
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.connection import Base


class DiscountTypeEnum(Enum):
    percent = "percent"
    fixed = "fixed"


class Discount(Base):
    __tablename__ = "discounts"

    title: Mapped[str]
    discount_type: Mapped[DiscountTypeEnum]
    value: Mapped[float]
    start_date: Mapped[datetime] = mapped_column()
    end_date: Mapped[datetime] = mapped_column()
    is_active: Mapped[bool]

    # products = relationship("Product", back_populates="discount")

    def __repr__(self):
        return self.title


@listens_for(Discount, "before_update")
def before_update_listener(mapper, connection, target):
    if target.start_date > target.end_date:
        raise HTTPException(
            status_code=400, detail="Конечная дата должна быть позже начальной"
        )
    if target.discount_type == "percent" and (target.value < 0 or target.value > 100):
        raise HTTPException(
            status_code=400,
            detail="Укажите процентное соотношение в переменную value от 0 до 100",
        )


@listens_for(Discount, "before_insert")
def before_insert_listener(mapper, connection, target):
    if target.start_date > target.end_date:
        raise HTTPException(
            status_code=400, detail="Конечная дата должна быть позже начальной"
        )
    if target.discount_type == "percent" and (target.value < 0 or target.value > 100):
        raise HTTPException(
            status_code=400,
            detail="Укажите процентное соотношение в переменную value от 0 до 100",
        )
