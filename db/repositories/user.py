from sqlalchemy import select

from db.connection import async_session
from db.models.users import User
from db.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    model = User

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar()
