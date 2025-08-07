from typing import Annotated

from fastapi import APIRouter, status, HTTPException, Depends

from common.errors import EmptyQueryResult
from common.pagination import PaginationParams
from dependecies.session import AsyncSessionDep
from models import Worker
from services.workers.query_builder.worker import WorkerQueryBuilder
from services.workers.schemas.filters import WorkerFilter
from services.workers.schemas.worker import (WorkerListResponseSchema, WorkerResponseSchema, WorkerCreateSchema,
                                             WorkerUpdateSchema)
from services.workers.errors import WorkerNotFound

workers_router = APIRouter()


@workers_router.get('/workers')
async def get_workers(session: AsyncSessionDep,
                      pagination_params: Annotated[PaginationParams, Depends(PaginationParams)],
                      name_filter: WorkerFilter = Depends()) -> WorkerListResponseSchema:
    try:
        workers = await WorkerQueryBuilder.get_workers(session, pagination_params, name_filter)
        return WorkerListResponseSchema(items=workers)
    except EmptyQueryResult:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@workers_router.get('/worker_by_id/{id}')
async def get_worker_by_id(session: AsyncSessionDep, worker_id: int) -> WorkerResponseSchema:
    try:
        worker = await WorkerQueryBuilder.get_worker_by_id(session, worker_id)
        return worker
    except WorkerNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@workers_router.post('/workers', status_code=status.HTTP_201_CREATED)
async def create_worker(session: AsyncSessionDep, data: WorkerCreateSchema) -> WorkerResponseSchema:
    new_worker = await WorkerQueryBuilder.create_worker(session, data)
    return new_worker


@workers_router.delete('/worker_by_id/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_worker_by_id(session: AsyncSessionDep, worker_id: int) -> None:
    try:
        await WorkerQueryBuilder.delete_worker(session, worker_id)
    except WorkerNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@workers_router.patch('/worker_by_id/{worker_id}', response_model=Worker, status_code=status.HTTP_200_OK)
async def update_worker(session: AsyncSessionDep,
                        worker_id: int, data: WorkerUpdateSchema) -> WorkerResponseSchema:
    try:
        worker = await WorkerQueryBuilder.update_worker(session, worker_id, data)
        return worker
    except WorkerNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
