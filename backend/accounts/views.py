from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import UserSerializer, RegisterSerializer

User = get_user_model()

# Durée de vie du cookie refresh (doit correspondre à SIMPLE_JWT)
_REFRESH_COOKIE_MAX_AGE = int(
    settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()
)
_REFRESH_COOKIE_PATH = '/api/v1/auth/token/'


def _set_refresh_cookie(response, token):
    """Pose le cookie HttpOnly refresh_token."""
    response.set_cookie(
        'refresh_token',
        token,
        max_age=_REFRESH_COOKIE_MAX_AGE,
        httponly=True,
        secure=not settings.DEBUG,
        samesite='Lax',
        path=_REFRESH_COOKIE_PATH,
    )


class CookieTokenObtainPairView(TokenObtainPairView):
    """Login : renvoie l'access token dans le body, le refresh dans un cookie HttpOnly."""
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'auth_token'

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            refresh = response.data.pop('refresh', None)
            if refresh:
                _set_refresh_cookie(response, refresh)
        return response


class CookieTokenRefreshView(APIView):
    """Renouvelle l'access token via le cookie refresh_token HttpOnly."""
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        refresh = request.COOKIES.get('refresh_token')
        if not refresh:
            return Response(
                {'detail': 'Cookie de rafraîchissement absent. Veuillez vous reconnecter.'},
                status=401,
            )
        serializer = TokenRefreshSerializer(data={'refresh': refresh})
        serializer.is_valid(raise_exception=True)

        response = Response({'access': serializer.validated_data['access']})

        # Rotation du cookie si ROTATE_REFRESH_TOKENS = True
        new_refresh = serializer.validated_data.get('refresh')
        if new_refresh:
            _set_refresh_cookie(response, new_refresh)

        return response


class LogoutView(APIView):
    """Déconnexion : supprime le cookie refresh_token."""
    permission_classes = [permissions.AllowAny]

    def post(self, _request):
        response = Response({'detail': 'Déconnecté avec succès.'})
        response.delete_cookie('refresh_token', path=_REFRESH_COOKIE_PATH)
        return response


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'auth_token'


class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
