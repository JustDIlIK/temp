from sqlalchemy import select, inspect

from db.connection import async_session
from db.models.socials import Social
from db.repositories.base import BaseRepository


class SocialRepository(BaseRepository):
    model = Social

    @classmethod
    async def get_all(cls):
        async with async_session() as session:
            query = select(cls.model).filter_by(is_available=True)
            result = await session.execute(query)
            return result.scalars().all()
