import asyncio
import asyncpg
import datetime
from simple_print import sprint
from settings import POSTGRES_URI


async def db_init():
    # docker exec -i chat-interface python run src.database "db_init"
    conn = await asyncpg.connect(POSTGRES_URI)
    await conn.execute('''
        DROP TABLE IF EXISTS messages;
        CREATE TABLE messages (
            id serial PRIMARY KEY,
            author text,
            text text,
            creation_date date
        )
    ''')
    sprint("db_init -> success", c="green")
    await conn.close()
