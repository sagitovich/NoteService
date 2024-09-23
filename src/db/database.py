import logging
from asyncio import current_task, sleep
from sqlalchemy import MetaData, func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import (create_async_engine, AsyncSession, 
                                    async_sessionmaker, async_scoped_session)

from src.config import Config
from .models import Base, User, Note 

logger = logging.getLogger(__name__)


class Database():
    def __init__(self):
        self.engine = None 
        self.metadata = None
        self.session_maker = None
        self.scoped_session = None

    async def create_connection(self):
        self.engine = create_async_engine(Config.DATABASE_URL, echo=False)
        self.metadata = MetaData()

        self.session_maker = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        self.scoped_session = async_scoped_session(self.session_maker, scopefunc=current_task)

        async with self.engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)


    # async def create_db(self):
    #     while True:
    #         try:
    #             async with self.engine.begin() as connection:
    #                 status = await connection.run_sync(Base.metadata.create_all)
    #                 logger.debug(f'After: {status}\n{Base.metadata.create_all}')
    #                 if status:
    #                     break
    #                 else:
    #                     logger.error('No connection to DB')
    #                     await sleep(5)
    #         except Exception as e:
    #             logger.error(f'Error in /create_db: {e}')
                # await sleep(5)

    async def __aenter__(self):
        try:
            if self.scoped_session is None:
                raise Exception("Database is not defined")
            return self.scoped_session
        except Exception as e:
            logger.error(f'Error in /__aenter__: {e}')
    
    async def check_auth(self, login: str, password: str) -> str:
        try:
            async with self.scoped_session() as session:
                query = await session.execute(select(User).filter(User.login == login))
                user = query.scalar_one_or_none()

                if user and user.password == password:
                    return user.username  
                return None 
        except Exception as e:
            logger.error(f'Error in /check_auth: {e}')
        
    async def get_user_notes(self, username: str) -> list[User, Note]:
        try:
            async with self.scoped_session() as session:
                user_query = await session.execute(select(User).filter(User.username == username))
                user = user_query.scalar_one_or_none()

                if user:
                    notes_query = await session.execute(select(Note).filter(Note.user_id == user.id))
                    notes = notes_query.scalars().all()
                    return user, notes
                return None, []
        except Exception as e:
            logger.error(f'Error in /get_user_notes: {e}')

    async def add_note(self, username: str, content: str) -> Note:
        try:
            async with self.scoped_session() as session:
                user_query = await session.execute(select(User).filter(User.username == username))
                user = user_query.scalar_one_or_none()

                if not user:
                    return None

                max_id_query = await session.execute(select(func.coalesce(func.max(Note.id), 0)))
                max_id = max_id_query.scalar()

                new_note = Note(id=max_id + 1, content=content, user_id=user.id)
                session.add(new_note)
                await session.commit()
                return new_note
        except Exception as e:
            logger.error(f'Error in /add_note: {e}')
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try: 
            await self.scoped_session.remove()
        except Exception as e:
            logger.error(f'Error in /__aexit__: {e}')
