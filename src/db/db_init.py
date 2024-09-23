import logging
import asyncio

from .database import Database

logger = logging.getLogger(__name__)

async def init_db():
    db = Database()
    exist = False
    while not exist:
        try:
            await db.create_connection()
            logger.info('DB has successful connection')
            exist = True
        except Exception as e:
            logger.error(f'Error connection to DB: {e}')
            await asyncio.sleep(5)
    return db
