from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton

from jwt.jwt_service import JWTService, get_jwt_service


class AuthContainer(DeclarativeContainer):
    jwt_service: JWTService = Singleton(get_jwt_service)
