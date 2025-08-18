from fastapi import APIRouter, HTTPException, status, Depends

from models import User
from common.errors import EmptyQueryResult
from dependecies.session import AsyncSessionDep
from services.users.modules.manager import fastapi_users, auth_backend
from services.users.schemas.users import UserRead, UserCreate, UserUpdate
from services.users.query_builder.users import UserQueryBuilder
from services.users.modules.manager import current_active_user
from services.vacancies.schemas.vacancy import VacancyListResponseSchema

users_router = APIRouter()


users_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/users/jwt',
    tags=['users']
)
users_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/users',
    tags=['users']
)
users_router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix='/users',
    tags=['users']
)
users_router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix='/users',
    tags=['users']
)
users_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix='/users',
    tags=['users']
)


@users_router.get('/user/{id}/vacancies')
async def get_vacancies_of_user(session: AsyncSessionDep, user_id: int,
                                user: User = Depends(current_active_user)) -> VacancyListResponseSchema:
    try:
        vacancies = await UserQueryBuilder.get_vacancies_of_user(session, user_id)
        print(f"User {user.email} has sent a request")
        return VacancyListResponseSchema(items=vacancies)
    except EmptyQueryResult as e:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=str(e))
