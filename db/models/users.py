from sqlalchemy import String, Column, Integer
from sqlalchemy.orm import Mapped

from db.connection import Base


class User(Base):
    __tablename__ = "users"

    email: Mapped[str]
    password: Mapped[str]
