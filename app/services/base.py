from typing import Type
from bson import ObjectId, errors
from motor.core import AgnosticCollection
from app.core.exceptions import BaseHTTPException
from app.services import MongoService


class BaseService:
    collection_name: str
    not_found_error: Type[BaseHTTPException]

    def __init__(self, mongo_service: MongoService) -> None:
        self.mongo_service = mongo_service
        self.collection = self._get_collection()

    def _get_collection(self) -> AgnosticCollection:
        return self.mongo_service.get_collection(self.collection_name)

    def _get_id(self, id: str) -> ObjectId:
        try:
            object_id = ObjectId(id)
            return object_id
        except errors.InvalidId:
            raise self.not_found_error(id)
