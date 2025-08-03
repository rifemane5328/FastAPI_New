from typing import List, Optional
from fastapi import Query

from sqlmodel import select, delete
from dependecies.session import AsyncSessionDep
from models import Vacancy
from common.errors import EmptyQueryResult
from services.vacancies.schemas.vacancy import VacancyCreateSchema
from services.vacancies.errors import VacancyNotFound, ImpossibleRange


class VacancyQueryBuilder:
    @staticmethod
    async def get_vacancies(session: AsyncSessionDep, s_from: Optional[float] = Query(0.00, description="salary_from"),
                            s_to: Optional[float] = Query(25000.00, description="salary_to")) -> List[Vacancy]:
        query = select(Vacancy)
        result = await session.execute(query)
        vacancies = list(result.scalars())
        if not vacancies:
            raise EmptyQueryResult
        if s_from or s_to or s_from and s_to:
            vacancies_s = await VacancyQueryBuilder.get_vacancy_by_salary(session, s_from, s_to)
            return vacancies_s
        return vacancies

    @staticmethod
    async def get_vacancy_by_id(session: AsyncSessionDep, vacancy_id: int) -> Vacancy:
        query = select(Vacancy).where(vacancy_id == Vacancy.id)
        result = await session.execute(query)
        vacancy = result.scalar()
        if not vacancy:
            raise VacancyNotFound
        return vacancy

    @staticmethod
    async def get_vacancy_by_salary(session: AsyncSessionDep,
                                    s_from: Optional[float] = Query(0.00, description="salary_from"),
                                    s_to: Optional[float] = Query(25000.00, description="salary_to")) -> List[Vacancy]:
        if s_from > s_to:
            raise ImpossibleRange
        salary_filters = []
        if s_from:
            salary_filters.append(Vacancy.salary >= s_from)
        elif s_to:
            salary_filters.append(Vacancy.salary <= s_to)

        query = select(Vacancy).where(*salary_filters)
        result = await session.execute(query)
        vacancies = list(result.scalars())
        if not vacancies:
            raise EmptyQueryResult
        return vacancies

    @staticmethod
    async def create_vacancy(session: AsyncSessionDep, data: VacancyCreateSchema) -> Vacancy:
        vacancy = Vacancy(title=data.title, description=data.description, created_at=data.created_at,
                          salary=data.salary, worker_id=data.worker_id)
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
