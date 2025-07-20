from typing import List

from sqlmodel import select
from dependecies.session import AsyncSessionDep
from common.errors import EmptyQueryResult
from models import Worker
from services.workers.schemas.worker import WorkerCreateSchema


class WorkerQueryBuilder:
    @staticmethod
    async def get_workers(session: AsyncSessionDep) -> List[Worker]:
        query = select(Worker)
        result = await session.execute(query)
        workers = list(result.scalars())
        if not workers:
            raise EmptyQueryResult
        return workers

    @staticmethod
    async def create_worker(session: AsyncSessionDep, data: WorkerCreateSchema) -> Worker:
        worker = Worker(name=data.name, last_name=data.last_name, biography=data.biography, birth_date=data.birth_date)
        session.add(worker)
        await session.commit()
        await session.refresh(worker)
        return worker
