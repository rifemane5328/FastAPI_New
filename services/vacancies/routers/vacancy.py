from typing import Annotated
from fastapi import APIRouter, status, HTTPException, Query, Depends

from dependecies.session import AsyncSessionDep
from services.vacancies.schemas.vacancy import VacancyResponseSchema, VacancyListResponseSchema, VacancyCreateSchema
from services.vacancies.query_builder.vacancy import VacancyQueryBuilder
from common.errors import EmptyQueryResult
from common.pagination import PaginationParams
from services.vacancies.errors import VacancyNotFound, ImpossibleRange
from services.vacancies.schemas.filters import VacancyFilter


vacancies_router = APIRouter()


@vacancies_router.get('/vacancies')
async def get_vacancies(session: AsyncSessionDep,
                        pagination_params: Annotated[PaginationParams, Depends(PaginationParams)],
                        title_filter: VacancyFilter = Depends(),
                        s_from: float = Query(0.00, description="salary_from"),
                        s_to: float = Query(25000.00, description="salary_to"),
                        ) -> VacancyListResponseSchema:
    try:
        vacancies = await VacancyQueryBuilder.get_vacancies(session, pagination_params, title_filter, s_from, s_to)
        return VacancyListResponseSchema(items=vacancies)
    except EmptyQueryResult:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    except VacancyNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ImpossibleRange as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@vacancies_router.get('/vacancy_by_id/{id}')
async def get_vacancy_by_id(session: AsyncSessionDep, vacancy_id: int) -> VacancyResponseSchema:
    try:
        new_vacancy = await VacancyQueryBuilder.get_vacancy_by_id(session, vacancy_id)
        return new_vacancy
    except VacancyNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@vacancies_router.post('/vacancies')
async def create_vacancy(session: AsyncSessionDep, data: VacancyCreateSchema) -> VacancyResponseSchema:
    new_vacancy = await VacancyQueryBuilder.create_vacancy(session, data)
    return new_vacancy


@vacancies_router.delete('/vacancy_by_id/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_vacancy_by_id(session: AsyncSessionDep, vacancy_id: int) -> None:
    try:
        await VacancyQueryBuilder.delete_vacancy_by_id(session, vacancy_id)
    except VacancyNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
