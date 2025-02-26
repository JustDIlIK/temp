from db.models.shop import Shop
from db.repositories.base import BaseRepository


class ShopRepository(BaseRepository):
    model = Shop
