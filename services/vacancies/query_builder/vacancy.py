from typing import List, Optional
from fastapi import Query
from sqlalchemy import Select
from sqlalchemy.orm import selectinload

from sqlmodel import select, delete
from dependecies.session import AsyncSessionDep
from models import Vacancy
from common.errors import EmptyQueryResult
from common.pagination import PaginationParams
from services.vacancies.schemas.vacancy import VacancyCreateSchema, VacancyUpdateSchema
from services.vacancies.errors import VacancyNotFound, ImpossibleRange
from services.vacancies.schemas.filters import VacancyFilter


class VacancyQueryBuilder:
    @staticmethod
    async def get_vacancies(session: AsyncSessionDep, pagination_params: PaginationParams,
                            title_filter: Optional[VacancyFilter] = None,
                            s_from: Optional[float] = None, s_to: Optional[float] = None) -> List[Vacancy]:

        query_offset, query_limit = (pagination_params.page - 1) * pagination_params.size, pagination_params.size
        select_query = await VacancyQueryBuilder.apply_filters(select(Vacancy), title_filter, s_from, s_to)
        select_query = select_query.offset(query_offset).limit(query_limit)
        result = await session.execute(select_query)
        vacancies = list(result.scalars())
        if not vacancies:
            raise EmptyQueryResult
        return vacancies

    @staticmethod
    async def apply_filters(select_query: Select, title_filter: VacancyFilter,
                            s_from: Optional[float] = Query(0.00, description="salary_from"),
                            s_to: Optional[float] = Query(25000.00, description="salary_to")) -> Select:
        if s_from > s_to:
            raise ImpossibleRange
        if s_from:
            select_query = select_query.where(Vacancy.salary >= s_from)
        if s_to:
            select_query = select_query.where(Vacancy.salary <= s_to)
        if title_filter and title_filter.title:
            select_query = select_query.where(Vacancy.title.ilike(f'%{title_filter.title}%'))
        return select_query

    @staticmethod
    async def get_vacancy_by_id(session: AsyncSessionDep, vacancy_id: int) -> Vacancy:
        query = select(Vacancy).where(vacancy_id == Vacancy.id)
        result = await session.execute(query)
        vacancy = result.scalar()
        if not vacancy:
            raise VacancyNotFound
        return vacancy

    @staticmethod
    async def create_vacancy(session: AsyncSessionDep, data: VacancyCreateSchema) -> Vacancy:
        vacancy = Vacancy(title=data.title, description=data.description, created_at=data.created_at,
                          salary=data.salary, worker_id=data.worker_id, user_id=data.user_id)
        session.add(vacancy)
        await session.commit()
        await session.refresh(vacancy)
        return vacancy

    @staticmethod
    async def delete_vacancy_by_id(session: AsyncSessionDep, vacancy_id: int) -> None:
        await VacancyQueryBuilder.get_vacancy_by_id(session, vacancy_id)

        query = delete(Vacancy).where(vacancy_id == Vacancy.id)
        await session.execute(query)
        await session.commit()

    @staticmethod
    async def update_vacancy(session: AsyncSessionDep, vacancy_id: int, data: VacancyUpdateSchema) -> Vacancy:
        vacancy = await VacancyQueryBuilder.get_vacancy_by_id(session, vacancy_id)
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(vacancy, key, value)
        await session.commit()
        await session.refresh(vacancy)
        return vacancy

    @staticmethod
    async def update_vacancy_fully(session: AsyncSessionDep, vacancy_id: int, data: VacancyCreateSchema) -> Vacancy:
        vacancy = await VacancyQueryBuilder.get_vacancy_by_id(session, vacancy_id)
        for key, value in data.model_dump().items():
            setattr(vacancy, key, value)
        await session.commit()
        await session.refresh(vacancy)
        return vacancy

    @staticmethod
    async def get_vacancies_of_user(session: AsyncSessionDep, user_id: int) -> List[Vacancy]:
        select_query = select(Vacancy).where(Vacancy.user_id == user_id)
        query_result = await session.execute(select_query)
        vacancies = list(query_result.scalars())
        if not vacancies:
            raise EmptyQueryResult
        return vacancies
