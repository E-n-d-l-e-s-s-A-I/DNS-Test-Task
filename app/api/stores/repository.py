from .models import Store
from app.utils.repository import BaseRepository


class StoreRepository(BaseRepository):
    model = Store
