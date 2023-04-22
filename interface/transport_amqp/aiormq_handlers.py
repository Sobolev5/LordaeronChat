import aiormq
import time
import asyncio
from src import methods
from src import schema
from settings import AMQP_URI
from simple_print import sprint
from .helpers import validate_schema
from pydantic import BaseModel
from carrot import carrot_ask


@validate_schema(schema.Health)
async def health(request: dict):
    response = await methods.health(request)
    return response


class HelloCarrot(BaseModel):
    ping: int


@carrot_ask(HelloCarrot)
async def carrot_called(incoming_dict: dict) -> dict:
    sprint(incoming_dict, c="green")
    d = {}
    d["pong"] = 1
    return d


async def consume():
    
    try:
        connection = await aiormq.connect(AMQP_URI)
        channel = await connection.channel()
        await channel.basic_qos(prefetch_count=3)
        sprint(f"AMQP CONSUMER:     ready to recieve [YES] Basic QOS=3", c="green", p=1)

        # health 
        declare_ok = await channel.queue_declare(f"interface:health", durable=True)
        await channel.basic_consume(declare_ok.queue, health, no_ack=False)

        # carrot ask
        declare_ok = await channel.queue_declare(f"interface:carrot_call", durable=True)  
        await channel.basic_consume(declare_ok.queue, carrot_called, no_ack=False)  
        
    except Exception as e:
        sprint(f"AMQP CONSUMER:     try to reconnect error={e}", c="red", p=1)
        time.sleep(3)
        asyncio.create_task(consume())
    


        

