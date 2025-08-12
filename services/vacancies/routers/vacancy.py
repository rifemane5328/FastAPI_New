from typing import Annotated
from fastapi import APIRouter, status, HTTPException, Query, Depends

from dependecies.session import AsyncSessionDep
from models import Vacancy
from models import User
from services.vacancies.schemas.vacancy import VacancyResponseSchema, VacancyListResponseSchema, VacancyCreateSchema, \
    VacancyUpdateSchema
from services.vacancies.query_builder.vacancy import VacancyQueryBuilder
from common.errors import EmptyQueryResult
from common.pagination import PaginationParams
from services.vacancies.errors import VacancyNotFound, ImpossibleRange
from services.vacancies.schemas.filters import VacancyFilter
from services.users.modules.manager import current_active_user

vacancies_router = APIRouter()


@vacancies_router.get('/vacancies')
async def get_vacancies(session: AsyncSessionDep,
                        pagination_params: Annotated[PaginationParams, Depends(PaginationParams)],
                        title_filter: VacancyFilter = Depends(),
                        s_from: float = Query(0.00, description="salary_from"),
                        s_to: float = Query(25000.00, description="salary_to"),
                        user: User = Depends(current_active_user)
                        ) -> VacancyListResponseSchema:
    try:
        vacancies = await VacancyQueryBuilder.get_vacancies(session, pagination_params, title_filter, s_from, s_to)
        print(f"User {user.email} has sent a request")
        return VacancyListResponseSchema(items=vacancies)
    except EmptyQueryResult:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    except VacancyNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ImpossibleRange as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@vacancies_router.get('/vacancy_by_id/{id}')
async def get_vacancy_by_id(session: AsyncSessionDep, vacancy_id: int,
                            user: User = Depends(current_active_user)) -> VacancyResponseSchema:
    try:
        new_vacancy = await VacancyQueryBuilder.get_vacancy_by_id(session, vacancy_id)
        print(f"User {user.email} has sent a request")
        return new_vacancy
    except VacancyNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@vacancies_router.post('/vacancies')
async def create_vacancy(session: AsyncSessionDep, data: VacancyCreateSchema,
                         user: User = Depends(current_active_user)) -> VacancyResponseSchema:
    new_vacancy = await VacancyQueryBuilder.create_vacancy(session, data)
    print(f"User {user.email} has sent a request")
    return new_vacancy


@vacancies_router.delete('/vacancy_by_id/{id}', status_code=status.HTTP_204_NO_CONTENT,
                         response_description=f"User was successfully deleted")
async def delete_vacancy_by_id(session: AsyncSessionDep, vacancy_id: int,
                               user: User = Depends(current_active_user)) -> None:
    try:
        await VacancyQueryBuilder.delete_vacancy_by_id(session, vacancy_id)
        print(f"User {user.email} has sent a request")
    except VacancyNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@vacancies_router.patch('/vacancy_by_id/{id}', response_model=Vacancy, status_code=status.HTTP_200_OK)
async def update_vacancy(session: AsyncSessionDep, vacancy_id: int, data: VacancyUpdateSchema,
                         user: User = Depends(current_active_user)) -> VacancyResponseSchema:
    try:
        vacancy = await VacancyQueryBuilder.update_vacancy(session, vacancy_id, data)
        print(f"User {user.email} has sent a request")
        return vacancy
    except VacancyNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@vacancies_router.put('/vacancy_by_id/{vacancy_id}', response_model=Vacancy, status_code=status.HTTP_200_OK)
async def update_vacancy_fully(session: AsyncSessionDep, vacancy_id: int, data: VacancyCreateSchema,
                               user: User = Depends(current_active_user)) -> VacancyResponseSchema:
    try:
        vacancy = await VacancyQueryBuilder.update_vacancy_fully(session, vacancy_id, data)
        print(f"User {user.email} has sent a request")
        return vacancy
    except VacancyNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
