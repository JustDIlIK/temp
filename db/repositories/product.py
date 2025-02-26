from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from db.connection import async_session
from db.models.product import Product
from db.repositories.base import BaseRepository


class ProductRepository(BaseRepository):
    model = Product

    @classmethod
    async def get_all(cls, page=1, limit=500):
        async with async_session() as session:
            query = (
                select(cls.model)

                .offset((page - 1) * limit)
                .limit(limit)
                .filter(cls.model.new_price.isnot(None), cls.model.is_available==True)
                .order_by(cls.model.position, cls.model.id.desc())

            )

            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session() as session:
            query = select(cls.model)
            query = (
                query.filter(
                    (cls.model.title.ilike(f"%{filter_by["title"].lower()}%"))
                    | (
                        cls.model.description.ilike(
                            f"%{filter_by["description"].lower()}%"
                        )
                    )
                )
                .order_by(cls.model.id.desc())
            )

            result = await session.execute(query)
            return result.scalars().all()
