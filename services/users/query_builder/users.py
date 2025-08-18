from typing import List
from sqlmodel import select

from models import Vacancy
from dependecies.session import AsyncSessionDep
from common.errors import EmptyQueryResult


class UserQueryBuilder:
    @staticmethod
    async def get_vacancies_of_user(session: AsyncSessionDep, user_id: int) -> List[Vacancy]:
        select_query = select(Vacancy).where(Vacancy.user_id == user_id)
        query_result = await session.execute(select_query)
        vacancies = list(query_result.scalars())
        if not vacancies:
            raise EmptyQueryResult
        return vacancies
