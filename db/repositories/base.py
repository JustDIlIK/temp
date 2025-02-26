from sqlalchemy import select, insert, inspect
from sqlalchemy.orm import ONETOMANY, selectinload, joinedload

from db.connection import async_session


class BaseRepository:
    model = None

    @classmethod
    async def get_all(cls, page=1, limit=500):
        async with async_session() as session:
            query = (
                select(cls.model)
                .offset((page - 1) * limit)
                .limit(limit)
                .order_by(cls.model.id)
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

    @classmethod
    async def get_by_id(cls, id):
        async with async_session() as session:
            query = select(cls.model).filter_by(id=id)

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

            return result.scalars().first()

    @classmethod
    async def add_record(cls, **data):
        async with async_session() as session:
            query = insert(cls.model).values(data).returning(cls.model)
            result = await session.execute(query)
            await session.commit()
            return result.scalar()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.first()
