import time
import asyncio
import aiormq
from pydantic import BaseModel
from simple_print import sprint
from carrot import carrot_ask
from starlette.applications import Starlette
from settings import AMQP_URI


class BotTalk(BaseModel):
    author: str
    text: str


@carrot_ask(BotTalk)
async def bot_talk(incoming_dict: dict) -> dict:
    sprint(incoming_dict, c="green")
    time.sleep(2)
    outcoming_dict = {}
    outcoming_dict["author"] = "Answer from Bot"
    outcoming_dict["text"] = "Bloog Gives me power"
    if incoming_dict["author"] == "Orc":
        reply_dict["text"] = "Go away from Lordaeron!"    

    return outcoming_dict


# make amqp router:
async def consume():
    try:
        connection = await aiormq.connect(AMQP_URI)
        channel = await connection.channel()
        await channel.basic_qos(prefetch_count=3)
        sprint(f"AMQP CONSUMER:     ready to recieve [YES] Basic QOS=3", c="green", p=1)

        # talk with interface 
        declare_ok = await channel.queue_declare(f"bot:talk", durable=True)
        await channel.basic_consume(declare_ok.queue, bot_talk, no_ack=False)
        
    except Exception as e:
        sprint(f"AMQP CONSUMER:     try to reconnect error={e}", c="red", p=1)
        time.sleep(3)
        asyncio.create_task(consume())
    

class AppWithAMQP(Starlette):
    def __init__(self, *args, **kwargs):
        loop = asyncio.get_event_loop()
        loop.create_task(consume())
        super().__init__(*args, **kwargs)

app = AppWithAMQP()