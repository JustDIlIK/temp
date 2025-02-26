from sqlalchemy import select, inspect
from sqlalchemy.orm import ONETOMANY, selectinload, joinedload

from db.connection import async_session
from db.models.discount import Discount
from db.repositories.base import BaseRepository


class DiscountRepository(BaseRepository):
    model = Discount

    @classmethod
    async def get_all(cls, page=1, limit=500):
        async with async_session() as session:
            query = (
                select(cls.model)
                .offset((page - 1) * limit)
                .limit(limit)
                .order_by(cls.model.id.desc())
            ).filter_by(is_active=True)

            mapper = inspect(cls.model)
            relationships = mapper.relationships
            fields = relationships.keys()
            load_options = []
            for field in fields:
                rel_property = relationships[field]
                direction = rel_property.direction
                use_list = rel_property.uselist
                if direction == ONETOMANY or use_list is False:
                    loader = selectinload(getattr(cls.model, field))
                else:
                    loader = joinedload(getattr(cls.model, field))

                load_options.append(loader)

            query = query.options(*load_options)
            result = await session.execute(query)
            return result.scalars().all()
