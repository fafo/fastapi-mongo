from fastapi import Request
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.db import MongoDBUserDatabase
from models.users import User, UserDB, UserCreate, UserUpdate
from db.mongo import get_db
from settings import settings

import logging
LOG = logging.getLogger(__name__)


def on_register(user: UserDB, request: Request):
    LOG.debug("registered: " + user.json())


user_db = MongoDBUserDatabase(UserDB, get_db(settings.APP_DB)["users"])
jwt_authentication = JWTAuthentication(
    secret=settings.JWT_SECRET,
    lifetime_seconds=settings.JWT_LIFETIME,
    tokenUrl="/auth/jwt/login"
)

# setup users
fastapi_users = FastAPIUsers(
    user_db, [jwt_authentication], User, UserCreate, UserUpdate, UserDB)


def setup_users(app):

    app.include_router(
        fastapi_users.get_auth_router(jwt_authentication),
        prefix="/auth/jwt", tags=["auth"]
    )

    app.include_router(
        fastapi_users.get_register_router(on_register),
        prefix="/auth", tags=["auth"]
    )

    app.include_router(
        fastapi_users.get_reset_password_router(
            # SECRET, after_forgot_password=on_after_forgot_password
            settings.JWT_SECRET
        ),
        prefix="/auth",
        tags=["auth"]
    )

    app.include_router(
        fastapi_users.get_users_router(), prefix="/users", tags=["users"])

    # todo: refresh
    # https://frankie567.github.io/fastapi-users/configuration/authentication/jwt/
    # from fastapi import Depends, Response
    # @router.post("/auth/jwt/refresh")
    # async def refresh_jwt(response: Response, user=Depends(fastapi_users.get_current_active_user)):
    #     return await jwt_authentication.get_login_response(user, response)
