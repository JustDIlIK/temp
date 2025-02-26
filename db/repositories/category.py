from db.models.category import Category
from db.repositories.base import BaseRepository


class CategoryRepository(BaseRepository):
    model = Category
