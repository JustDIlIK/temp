from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from db.connection import Base


class Condition(Base):
    __tablename__ = "conditions"

    title: Mapped[str]
    title_uz: Mapped[str] = mapped_column(nullable=True)

    position: Mapped[int]
