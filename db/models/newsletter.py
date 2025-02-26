from sqlalchemy.orm import Mapped

from db.connection import Base


class Newsletter(Base):
    __tablename__ = "newsletter"

    email: Mapped[str]
