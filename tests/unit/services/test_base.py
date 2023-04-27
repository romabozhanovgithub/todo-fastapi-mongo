import pytest

from app.services.base import BaseService


@pytest.mark.asyncio
async def test_create_document(base_service: BaseService):
    document = {"name": "test"}
    new_document = await base_service.create_document(document)
    assert new_document["name"] == document["name"]
    assert new_document["created_at"] is not None
