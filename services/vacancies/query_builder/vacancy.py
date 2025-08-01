from typing import List

from sqlmodel import select, delete
from dependecies.session import AsyncSessionDep
from models import Vacancy
from common.errors import EmptyQueryResult
from services.vacancies.schemas.vacancy import VacancyCreateSchema
from services.vacancies.errors import VacancyNotFound, ImpossibleRange


class VacancyQueryBuilder:
    @staticmethod
    async def get_vacancies(session: AsyncSessionDep, vacancy_id: int | None = None, s_from: float | None = None,
                            s_to: float | None = None) -> List[Vacancy]:
        query = select(Vacancy)
        result = await session.execute(query)
        vacancies = list(result.scalars())
        if not vacancies:
            raise EmptyQueryResult
        if vacancy_id:
            vacancy = VacancyQueryBuilder.get_vacancy_by_id(session, vacancy_id)
            return vacancy
        if s_from and s_to:
            vacancies_s = VacancyQueryBuilder.get_vacancy_by_salary(session, s_from, s_to)
            return vacancies_s
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
    async def get_vacancy_by_id(session: AsyncSessionDep, vacancy_id: int) -> Vacancy:
        query = select(Vacancy).where(vacancy_id == Vacancy.id)
        result = await session.execute(query)
        vacancy = result.scalar()
        if not vacancy:
            raise VacancyNotFound
        return vacancy

    @staticmethod
    async def delete_vacancy_by_id(session: AsyncSessionDep, vacancy_id: int) -> None:
        await VacancyQueryBuilder.get_vacancy_by_id(session, vacancy_id)

        query = delete(Vacancy).where(vacancy_id == Vacancy.id)
        await session.execute(query)
        await session.commit()

    @staticmethod
    async def get_vacancy_by_salary(session: AsyncSessionDep, s_from: float, s_to: float) -> List[Vacancy]:
        query = select(Vacancy).where(Vacancy.salary >= s_from, Vacancy.salary <= s_to)
        if s_from > s_to:
            raise ImpossibleRange
        result = await session.execute(query)
        vacancies = list(result.scalars())
        if not vacancies:
            raise VacancyNotFound
        return vacancies
