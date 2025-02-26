from db.models.newsletter import Newsletter
from db.repositories.base import BaseRepository


class NewsletterRepository(BaseRepository):
    model = Newsletter
