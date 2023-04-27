import pytest

from app.services.base import BaseService


@pytest.mark.asyncio
async def test_create_document(base_service: BaseService):
    document = {"name": "test"}
    new_document = await base_service.create_document(document)
    assert new_document["name"] == document["name"]
    assert new_document["created_at"] is not None


@pytest.mark.asyncio
async def test_find_document_by_id(base_service: BaseService):
    document = {"name": "test"}
    new_document = await base_service.create_document(document)
    found_document = await base_service.find_document_by_id(str(new_document["_id"]))
    assert found_document["name"] == document["name"]
    assert found_document["created_at"] is not None


@pytest.mark.asyncio
async def test_find_document_by_id_not_found(base_service: BaseService):
    with pytest.raises(base_service.not_found_exception):
        await base_service.find_document_by_id("5f5b9c5e0f8f0b2c2f2d6f6f")


@pytest.mark.asyncio
async def test_find_document_by_id_invalid_id(base_service: BaseService):
    with pytest.raises(base_service.not_found_exception):
        await base_service.find_document_by_id("invalid_id")


@pytest.mark.asyncio
async def test_find_document_by_id_with_filter(base_service: BaseService):
    document = {"name": "test"}
    new_document = await base_service.create_document(document)
    found_document = await base_service.find_document_by_id(
        str(new_document["_id"]), {"name": "test"}
    )
    assert found_document["name"] == document["name"]
    assert found_document["created_at"] is not None


@pytest.mark.asyncio
async def test_find_document_by_id_with_filter_not_found(base_service: BaseService):
    document = {"name": "test"}
    new_document = await base_service.create_document(document)
    with pytest.raises(base_service.not_found_exception):
        await base_service.find_document_by_id(
            str(new_document["_id"]), {"name": "invalid"}
        )


@pytest.mark.asyncio
async def test_find_document_by_id_with_filter_invalid_id(base_service: BaseService):
    with pytest.raises(base_service.not_found_exception):
        await base_service.find_document_by_id(
            "invalid_id", {"name": "invalid"}
        )


@pytest.mark.asyncio
async def test_find_document_by_id_with_filter_invalid_filter(
    base_service: BaseService,
):
    with pytest.raises(base_service.not_found_exception):
        await base_service.find_document_by_id(
            "5f5b9c5e0f8f0b2c2f2d6f6f", {"invalid": "invalid"}
        )


@pytest.mark.asyncio
async def test_find_document_by_id_with_filter_invalid_filter_value(
    base_service: BaseService,
):
    with pytest.raises(base_service.not_found_exception):
        await base_service.find_document_by_id(
            "5f5b9c5e0f8f0b2c2f2d6f6f", {"name": "invalid"}
        )


@pytest.mark.asyncio
async def test_find_document_by_id_with_filter_invalid_filter_value_type(
    base_service: BaseService,
):
    with pytest.raises(base_service.not_found_exception):
        await base_service.find_document_by_id(
            "5f5b9c5e0f8f0b2c2f2d6f6f", {"name": 1}
        )


@pytest.mark.asyncio
async def test_find_documents(base_service: BaseService):
    document = {"name": "test"}
    await base_service.create_document(document)
    documents = await base_service.find_documents()
    assert len(documents) > 0


@pytest.mark.asyncio
async def test_find_documents_with_invalid_filter(base_service: BaseService):
    documents = await base_service.find_documents({"invalid": "invalid"})
    assert len(documents) == 0


@pytest.mark.asyncio
async def test_find_and_update_document_by_id(base_service: BaseService):
    document = {"name": "test"}
    new_document = await base_service.create_document(document)
    updated_document = await base_service.find_and_update_document_by_id(
        str(new_document["_id"]), {"name": "test2"}
    )
    assert updated_document["name"] == "test2"
    assert updated_document["created_at"] is not None


@pytest.mark.asyncio
async def test_find_and_update_document_by_id_not_found(base_service: BaseService):
    with pytest.raises(base_service.not_found_exception):
        await base_service.find_and_update_document_by_id(
            "5f5b9c5e0f8f0b2c2f2d6f6f", {"name": "test2"}
        )


@pytest.mark.asyncio
async def test_find_and_delete_document_by_id(base_service: BaseService):
    document = {"name": "test"}
    new_document = await base_service.create_document(document)
    deleted_document = await base_service.find_and_delete_document_by_id(
        str(new_document["_id"])
    )
    assert deleted_document["name"] == document["name"]
    assert deleted_document["created_at"] is not None


@pytest.mark.asyncio
async def test_find_and_delete_document_by_id_not_found(base_service: BaseService):
    with pytest.raises(base_service.not_found_exception):
        await base_service.find_and_delete_document_by_id("5f5b9c5e0f8f0b2c2f2d6f6f")
