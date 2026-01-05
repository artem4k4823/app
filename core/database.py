from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from .config import settings

class DataBase:
    def __init__(self, url:str):
        self.engine = create_async_engine(
            url = url
        )

        self.session_factory = async_sessionmaker(
            bind = self.engine,
            autoflush=False,
            autocommit = False,
            expire_on_commit=False
        )
        
    async def session_getter(self):
        async with self.session_factory() as session:
            yield session
            await session.commit()
            
db = DataBase(
    url = settings.DATABASE_URL
)