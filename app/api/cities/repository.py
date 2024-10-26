from .models import City
from app.utils.repository import BaseRepository


class CityRepository(BaseRepository):
    model = City
