from sqlalchemy import select

from db.connection import async_session
from db.models.promotion import Promotion
from db.repositories.base import BaseRepository


class PromotionRepository(BaseRepository):
    model = Promotion

    @classmethod
    async def get_all(cls, page=1, limit=500):
        async with async_session() as session:
            query = (
                select(cls.model)
                .offset((page - 1) * limit)
                .limit(limit)
                .order_by(cls.model.position, cls.model.id.desc())
            )

            result = await session.execute(query)
            return result.scalars().all()
