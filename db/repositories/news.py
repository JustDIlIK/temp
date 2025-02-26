from sqlalchemy import select, inspect
from sqlalchemy.orm import selectinload, ONETOMANY, joinedload

from db.connection import async_session
from db.models.news import News
from db.repositories.base import BaseRepository


class NewsRepository(BaseRepository):
    model = News

    @classmethod
    async def get_all(cls, page=1, limit=500):
        async with async_session() as session:
            query = (
                select(cls.model)
                .offset((page - 1) * limit)
                .limit(limit)
                .filter_by(is_active=True)
                .order_by(cls.model.created_at.desc())
            )

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
            print(load_options)

            query = query.options(*load_options)
            result = await session.execute(query)
            return result.scalars().all()
