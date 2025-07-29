from fastapi import APIRouter, status, HTTPException

from common.errors import EmptyQueryResult
from dependecies.session import AsyncSessionDep
from services.workers.query_builder.worker import WorkerQueryBuilder
from services.workers.schemas.worker import WorkerListResponseSchema, WorkerResponseSchema, WorkerCreateSchema
from services.workers.errors import WorkerNotFound

workers_router = APIRouter()


@workers_router.get('/workers')
async def get_workers(session: AsyncSessionDep) -> WorkerListResponseSchema:
    try:
        workers = await WorkerQueryBuilder.get_workers(session)
        return WorkerListResponseSchema(items=workers)
    except EmptyQueryResult:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@workers_router.post('/workers')
async def create_worker(session: AsyncSessionDep, data: WorkerCreateSchema) -> WorkerResponseSchema:
    new_worker = await WorkerQueryBuilder.create_worker(session, data)
    return new_worker


@workers_router.get('/worker_by_id/{id}')
async def get_worker_by_id(session: AsyncSessionDep, worker_id: int) -> WorkerResponseSchema:
    try:
        worker = await WorkerQueryBuilder.get_worker_by_id(session, worker_id)
        return worker
    except WorkerNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@workers_router.delete('/worker_by_id/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_worker_by_id(session: AsyncSessionDep, worker_id: int) -> None:
    try:
        await WorkerQueryBuilder.delete_worker(session, worker_id)
    except WorkerNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

