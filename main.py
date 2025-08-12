from contextlib import asynccontextmanager

from fastapi import FastAPI

from common.settings import Settings
from db.database import Database
from services.users.routers.users import users_router
from services.workers.routers.worker import workers_router
from services.vacancies.routers.vacancy import vacancies_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    database = Database(settings=Settings())
    yield
    await database.dispose(close=False)


app = FastAPI(lifespan=lifespan)


app.include_router(workers_router, tags=['workers, workers, worker_by_id, worker_by_id'])
app.include_router(vacancies_router, tags=['vacancies, vacancies, vacancy_by_id, vacancy_by_id'])
app.include_router(users_router)
