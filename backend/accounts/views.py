from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    UserSerializer,
    RegisterSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    ChangePasswordSerializer,
)

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
    """GET : profil courant. PATCH : mise à jour partielle (PUT désactivé)."""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'patch', 'head', 'options']

    def get_object(self):
        return self.request.user


class PasswordResetRequestView(APIView):
    """Envoie un email avec le lien de réinitialisation du mot de passe."""
    permission_classes = [permissions.AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'auth_token'

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        # Réponse identique que l'email existe ou non (anti-énumération)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail': 'Si cet email est enregistré, un lien a été envoyé.'})

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_url = (
            f'{settings.FRONTEND_URL}/reinitialiser-mot-de-passe'
            f'?uid={uid}&token={token}'
        )

        from .tasks import send_password_reset_email
        send_password_reset_email.delay(user.pk, reset_url)

        return Response({'detail': 'Si cet email est enregistré, un lien a été envoyé.'})


class PasswordResetConfirmView(APIView):
    """Valide le token et applique le nouveau mot de passe."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        user.set_password(serializer.validated_data['password'])
        user.save(update_fields=['password'])

        return Response({'detail': 'Mot de passe mis à jour avec succès.'})


class ChangePasswordView(APIView):
    """Change le mot de passe d'un utilisateur connecté."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save(update_fields=['password'])

        return Response(
            {'detail': 'Mot de passe modifié avec succès.'},
            status=status.HTTP_200_OK,
        )
