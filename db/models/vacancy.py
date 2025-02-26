from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from db.connection import Base


class Vacancy(Base):
    __tablename__ = "vacancies"

    title: Mapped[str]
    title_uz: Mapped[str] = mapped_column(nullable=True)

    description: Mapped[str]
    description_uz: Mapped[str] = mapped_column(nullable=True)

    address: Mapped[str]
    address_uz: Mapped[str] = mapped_column(nullable=True)
