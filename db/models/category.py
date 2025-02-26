from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.connection import Base


class Category(Base):
    __tablename__ = "categories"

    title: Mapped[str]
    description: Mapped[str]

    parent_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=True)

    #products = relationship("Product", back_populates="category")
    parent = relationship(
        "Category",
        remote_side="Category.id",
    )

    def __repr__(self):
        return f"Категория - {self.title}"
