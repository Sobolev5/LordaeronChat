import pytest
import aiormq
import orjson
from app import app
from src import schema
from src import methods
from transport_amqp import aiormq_handlers
from fastapi.testclient import TestClient
from settings import AMQP_URI


@pytest.mark.asyncio
async def create_record():
    request = {"check": 1}  

    validated_request = schema.Health.validate(request).dict()
    response = await methods.health(validated_request)
    assert response == {"ok": 200}


