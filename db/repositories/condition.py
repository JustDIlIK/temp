from db.models.conditions import Condition
from db.repositories.base import BaseRepository


class ConditionRepository(BaseRepository):
    model = Condition
