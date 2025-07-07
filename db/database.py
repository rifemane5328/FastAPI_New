from typing import Optional, Dict
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession, async_sessionmaker

from common.settings import Settings


class Database:
    def __init__(self, db_url: Optional[str | URL] = None,
                 engine_args: Optional[Dict] = None,
                 custom_engine: Optional[AsyncEngine] = None,
                 settings: Optional[Settings] = None
                 ):
        engine_args = engine_args or {}

        self._settings = settings or Settings()

        if custom_engine:
            self.engine = custom_engine
        else:
            if not db_url:
                db_url = self._settings.database.get_url()
                if not engine_args:
                    engine_args = dict(
                        echo=self._settings.database.debug
                    )
                self._engine = create_async_engine(db_url, **engine_args)  # type: ignore

            self._session_maker = async_sessionmaker(
                self._engine, class_=AsyncSession, expire_on_commit=False
            )
