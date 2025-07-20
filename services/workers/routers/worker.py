from fastapi import APIRouter, status, HTTPException

from common.errors import EmptyQueryResult
from dependecies.session import AsyncSessionDep
from services.workers.query_builder.worker import WorkerQueryBuilder
from services.workers.schemas.worker import WorkerListResponseSchema, WorkerResponseSchema, WorkerCreateSchema
from models import Worker

workers_router = APIRouter()


@workers_router.get('/workers')
async def get_workers_func(session: AsyncSessionDep) -> WorkerListResponseSchema:
    try:
        workers = await WorkerQueryBuilder.get_workers(session)
        return WorkerListResponseSchema(items=workers)
    except EmptyQueryResult:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@workers_router.post('/new_worker')
async def create_worker_func(session: AsyncSessionDep, data: WorkerCreateSchema) -> WorkerResponseSchema:
    new_worker = await WorkerQueryBuilder.create_worker(session, data)
    return new_worker
