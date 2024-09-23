import asyncio
from .database import Database

db = None


async def init_db():
    global db 
    while not db:
        try:
            db = Database()
            await db.create_db()
        except Exception:
            await asyncio.sleep(5)
