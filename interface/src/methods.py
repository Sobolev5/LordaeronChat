import asyncpg
import time
import orjson
import datetime
from carrot import CarrotCall
from simple_print import sprint
from channel_box import channel_box
from starlette.responses import JSONResponse
from settings import templates
from settings import POSTGRES_URI
from settings import AMQP_URI


async def call_bot(author, text, channel_name):
    carrot = await CarrotCall(AMQP_URI).connect()
    res = await carrot.call({"author": author, "text": text}, "bot:talk", timeout=5)  
    await channel_box.channel_send(channel_name="main", payload={"avatar": 5, **res})    


async def main(request):
    conn = await asyncpg.connect(POSTGRES_URI)
    room_name = request.path_params.get("room_name", "main")
    if request.method == "POST":
        async with request.form() as form:   
            author = form["author"]    
            text = form["text"]  

            await channel_box.channel_send(channel_name=room_name, payload={"author": author, "text": text, "avatar": 6} )               
            time.sleep(2)
            await call_bot(author, text, room_name)
            
            await conn.execute('INSERT INTO messages(author, text, creation_date) VALUES($1, $2, $3)', 
                author,
                text,
                datetime.datetime.now().date()        
            )
            sprint(f"Message {author} {text} added -> success", c="green")

            return JSONResponse({"200": "OK"})

    messages = await conn.fetch('SELECT * FROM messages')
    await conn.close()
    return templates.TemplateResponse('app.html', {'request': request, "room_name": room_name, "messages": messages})


async def check_socket_send(request):
    await channel_box.channel_send(channel_name="main", payload={"author": "def check_socket_send", "text": "hello from check_socket_send"})   
    return JSONResponse({"send": "success"})


async def check_carrot_call(request):
    d = {}
    d["ping"] = 1
    
    carrot = await CarrotCall(AMQP_URI).connect()
    res1 = await carrot.call(d, "interface:carrot_call", timeout=5)    

    carrot = await CarrotCall(AMQP_URI).connect()
    res2 = await carrot.call({"author": "footman", "text": "hello"}, "bot:talk", timeout=5)    

    return JSONResponse({"this_microserice":{**res1}, "microservice_bot":{**res2}})


async def health(data: dict) -> dict:
    return {"ok": 200}

