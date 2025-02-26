from db.models.vacancy import Vacancy
from db.repositories.base import BaseRepository


class VacancyRepository(BaseRepository):
    model = Vacancy
