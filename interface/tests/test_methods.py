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
async def test_health_without_transport():
    request = {"check": 1}  

    validated_request = schema.Health.validate(request).dict()
    response = await methods.health(validated_request)
    assert response == {"ok": 200}


def test_health_via_http():
    request = {"check": 1}  

    client = TestClient(app)    
    response = client.post(
        "/health",
        json=request,
    )   
    assert response.status_code == 200
    assert response.json() == {"ok": 200}


@pytest.mark.asyncio
async def test_health_via_amqp():
    request = {"check": 1}  

    request = orjson.dumps(request)
    connection = await aiormq.connect(AMQP_URI)
    channel = await connection.channel()
    declare_ok = await channel.queue_delete("interface:health")
    declare_ok = await channel.queue_declare("interface:health", durable=True)
    await channel.basic_publish(request, routing_key="interface:health")
    request = await channel.basic_get(declare_ok.queue)
    response = await aiormq_handlers.health(request)
    assert response == {"ok": 200}
    await connection.close()
