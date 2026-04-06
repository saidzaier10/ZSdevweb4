from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import InvalidToken


class OptionalJWTAuthentication(JWTAuthentication):
    """
    JWT authentication that returns anonymous user instead of 401
    when the token is invalid or expired. This allows AllowAny views
    to work even when the client sends a stale token.
    """

    def authenticate(self, request):
        try:
            return super().authenticate(request)
        except (AuthenticationFailed, InvalidToken):
            return None
