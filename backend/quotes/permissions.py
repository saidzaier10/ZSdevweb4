from rest_framework.permissions import BasePermission
from django.utils.crypto import constant_time_compare


class IsOwnerOrStaffOrValidToken(BasePermission):
    """
    Autorise l'accès à un devis si:
    - l'utilisateur est staff/admin, OU
    - le token fourni en query param correspond au signature_token du devis
    L'objet doit avoir un attribut `signature_token`.
    """

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_authenticated and request.user.is_staff:
            return True
        token = request.query_params.get('token', '')
        if token and obj.signature_token:
            return constant_time_compare(str(token), str(obj.signature_token))
        return False
