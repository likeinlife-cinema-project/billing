from aenum import StrEnum


class AuthEndPoint(StrEnum):
    API_V1 = "/api/v1/auth"
    SIGN_UP = f"{API_V1}/signup"
    SIGN_IN = f"{API_V1}/signin"
    LOGOUT = f"{API_V1}/logout"
    REFRESH = f"{API_V1}/refresh"
    LOGIN_HISTORY = f"{API_V1}/login_history"
