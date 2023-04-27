from datetime import datetime
from typing import Type
from bson import ObjectId, errors
from motor.core import AgnosticCollection

from app.core.exceptions import BaseHTTPException
from app.services import MongoService


class BaseService:
    collection_name: str
    not_found_exception: Type[BaseHTTPException]

    def __init__(self, mongo_service: MongoService) -> None:
        self.mongo_service = mongo_service
        self.collection = self._get_collection()

    def _get_collection(self) -> AgnosticCollection:
        return self.mongo_service.get_collection(self.collection_name)

    def _get_id(self, id: str) -> ObjectId:
        """
        This method is used to convert a string id to an ObjectId.
        Raises an exception if the id is invalid.
        """

        try:
            object_id = ObjectId(id)
            return object_id
        except errors.InvalidId:
            raise self.not_found_exception(id)

    async def create_document(self, document: dict) -> dict:
        """
        This method is used to create a document. It adds a created_at field.
        """

        result = await self.collection.insert_one(
            {**document, "created_at": datetime.utcnow()}
        )
        new_document = await self.find_document_by_id(result.inserted_id)
        return new_document

    async def find_document_by_id(self, id: str, filter: dict = {}) -> dict:
        """
        This method is used to find a document by id.
        Additional filters can be passed.
        Raises an exception if the document is not found.
        """

        document = await self.collection.find_one(
            {"_id": self._get_id(id), **filter}
        )
        if not document:
            raise self.not_found_exception(id)
        return document

    async def find_document_by_field(self, field: str, value: str) -> dict:
        """
        This method is used to find a document by field.
        Raises an exception if the document is not found.
        """

        document = await self.collection.find_one({field: value})
        if not document:
            raise self.not_found_exception(value)
        return document

    async def find_documents(
        self, filter: dict = {}, limit: int = 100
    ) -> list[dict]:
        """
        This method is used to find all documents.
        """

        documents = await self.collection.find(filter).to_list(length=limit)
        return documents

    async def find_and_update_document_by_id(
        self, id: str, update: dict, filter: dict = {}
    ) -> dict:
        """
        This method is used to update a document and return it.
        Additional filters can be passed.
        Raises an exception if the document is not found.
        """

        document = await self.collection.find_one_and_update(
            {"_id": self._get_id(id), **filter},
            {"$set": update},
            return_document=True,
        )
        if not document:
            raise self.not_found_exception(id)
        return document

    async def find_and_delete_document_by_id(
        self, id: str, filter: dict = {}
    ) -> dict:
        """
        This method is used to delete a document and return it.
        Additional filters can be passed.
        Raises an exception if the document is not found.
        """

        document = await self.collection.find_one_and_delete(
            {"_id": self._get_id(id), **filter}
        )
        if not document:
            raise self.not_found_exception(id)
        return document
