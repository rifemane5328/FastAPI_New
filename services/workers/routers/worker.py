from typing import Annotated

from fastapi import APIRouter, status, HTTPException, Depends

from common.errors import EmptyQueryResult
from common.pagination import PaginationParams
from dependecies.session import AsyncSessionDep
from models import Worker
from models import User
from services.workers.query_builder.worker import WorkerQueryBuilder
from services.workers.schemas.filters import WorkerFilter
from services.workers.schemas.worker import (WorkerListResponseSchema, WorkerResponseSchema, WorkerCreateSchema,
                                             WorkerUpdateSchema)
from services.workers.errors import WorkerNotFound, WorkerWithNameAlreadyExists
from services.users.modules.manager import current_active_user

workers_router = APIRouter()


@workers_router.get('/workers', response_model=WorkerListResponseSchema)
async def get_workers(session: AsyncSessionDep,
                      pagination_params: Annotated[PaginationParams, Depends(PaginationParams)],
                      name_filter: WorkerFilter = Depends(),
                      user: User = Depends(current_active_user)) -> WorkerListResponseSchema:
    try:
        workers = await WorkerQueryBuilder.get_workers(session, pagination_params, name_filter)
        print(f"User {user.email} has sent a request")
        return WorkerListResponseSchema(items=workers)
    except EmptyQueryResult:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@workers_router.get('/worker_by_id/{id}', response_model=Worker)
async def get_worker_by_id(session: AsyncSessionDep, worker_id: int,
                           user: User = Depends(current_active_user)) -> WorkerResponseSchema:
    try:
        worker = await WorkerQueryBuilder.get_worker_by_id(session, worker_id)
        print(f"User {user.email} has sent a request")
        return worker
    except WorkerNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@workers_router.post('/workers', status_code=status.HTTP_201_CREATED)
async def create_worker(session: AsyncSessionDep, data: WorkerCreateSchema,
                        user: User = Depends(current_active_user)) -> WorkerResponseSchema:
    try:
        worker = await WorkerQueryBuilder.create_worker(session, data)
        print(f"User {user.email} has created a new worker")
        return WorkerResponseSchema.model_validate(worker)
    except WorkerWithNameAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@workers_router.delete('/worker_by_id/{id}', status_code=status.HTTP_204_NO_CONTENT,
                       response_description=f"User was successfully deleted")
async def delete_worker_by_id(session: AsyncSessionDep, worker_id: int,
                              user: User = Depends(current_active_user)) -> None:
    try:
        await WorkerQueryBuilder.delete_worker(session, worker_id)
        print(f"User {user.email} has sent a request")
    except WorkerNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@workers_router.patch('/worker_by_id/{worker_id}', response_model=Worker, status_code=status.HTTP_200_OK)
async def update_worker(session: AsyncSessionDep, worker_id: int, data: WorkerUpdateSchema,
                        user: User = Depends(current_active_user)) -> WorkerResponseSchema:
    try:
        worker = await WorkerQueryBuilder.update_worker(session, worker_id, data)
        print(f"User {user.email} has sent a request")
        return worker
    except WorkerNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@workers_router.put('/worker_by_id/{worker_id}', response_model=Worker, status_code=status.HTTP_200_OK)
async def update_worker_fully(session: AsyncSessionDep, worker_id: int, data: WorkerCreateSchema,
                              user: User = Depends(current_active_user)) -> WorkerResponseSchema:
    try:
        worker = await WorkerQueryBuilder.update_worker_fully(session, worker_id, data)
        print(f"User {user.email} has sent a request")
        return worker
    except WorkerNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
