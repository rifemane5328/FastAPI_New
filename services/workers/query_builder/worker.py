from typing import List

from sqlmodel import select, delete
from dependecies.session import AsyncSessionDep
from common.errors import EmptyQueryResult
from models import Worker
from services.workers.schemas.worker import WorkerCreateSchema, WorkerUpdateSchema
from services.workers.errors import WorkerNotFound


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
    async def get_worker_by_id(session: AsyncSessionDep, worker_id: int) -> Worker:
        query = select(Worker).where(worker_id == Worker.id)
        result = await session.execute(query)
        worker = result.scalar()
        if not worker:
            raise WorkerNotFound
        return worker

    @staticmethod
    async def create_worker(session: AsyncSessionDep, data: WorkerCreateSchema) -> Worker:
        worker = Worker(name=data.name, last_name=data.last_name, biography=data.biography, birth_date=data.birth_date)
        session.add(worker)
        await session.commit()
        await session.refresh(worker)
        return worker

    @staticmethod
    async def delete_worker(session: AsyncSessionDep, worker_id: int) -> None:
        await WorkerQueryBuilder.get_worker_by_id(session, worker_id)

        query = delete(Worker).where(Worker.id == worker_id)
        await session.execute(query)
        await session.commit()
