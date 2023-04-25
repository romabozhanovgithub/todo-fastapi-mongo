from motor.core import AgnosticCollection
from app.services import MongoService


class BaseService:
    collection_name: str

    def __init__(
        self, mongo_service: MongoService
    ) -> None:
        self.mongo_service = mongo_service
        self.collection = self._get_collection()

    def _get_collection(self) -> AgnosticCollection:
        return self.mongo_service.get_collection(self.collection_name)
