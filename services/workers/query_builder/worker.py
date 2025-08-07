from typing import List, Optional

from sqlalchemy import Select

from sqlmodel import select, delete

from common.pagination import PaginationParams
from dependecies.session import AsyncSessionDep
from common.errors import EmptyQueryResult
from models import Worker
from services.workers.schemas.filters import WorkerFilter
from services.workers.schemas.worker import WorkerCreateSchema, WorkerUpdateSchema
from services.workers.errors import WorkerNotFound


class WorkerQueryBuilder:
    @staticmethod
    async def get_workers(session: AsyncSessionDep, pagination_params: PaginationParams,
                          name_filter: Optional[WorkerFilter] = None) -> List[Worker]:

        query_offset, query_limit = (pagination_params.page - 1) * pagination_params.size, pagination_params.size
        select_query = (WorkerQueryBuilder.apply_filters(select(Worker), name_filter).offset(query_offset)
                        .limit(query_limit))
        result = await session.execute(select_query)
        workers = list(result.scalars())
        if not workers:
            raise EmptyQueryResult
        return workers

    @staticmethod
    def apply_filters(select_query: Select, name_filter: WorkerFilter) -> Select:
        if name_filter and name_filter.name:
            select_query = select_query.where(Worker.name.ilike(f'%{name_filter.name}%'))
        return select_query

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

    @staticmethod
    async def update_worker(session: AsyncSessionDep, worker_id: int, data: WorkerUpdateSchema) -> Worker:
        worker = await WorkerQueryBuilder.get_worker_by_id(session, worker_id)
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(worker, key, value)
        await session.commit()
        await session.refresh(worker)
        return worker

