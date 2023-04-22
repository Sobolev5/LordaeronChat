import asyncio
from carrot import CarrotCall
from simple_print import sprint
from settings import AMQP_URI


async def carrot_call():
    # docker exec -i chat-interface python run transport_amqp.console "carrot_call"

    d = {}
    d["ping"] = 1

    carrot = await CarrotCall(AMQP_URI, DEBUG=True).connect()
    res = await carrot.call(d, "interface:carrot_call", timeout=5)    
    sprint(f'carrot_call -> {res}', c="green")

