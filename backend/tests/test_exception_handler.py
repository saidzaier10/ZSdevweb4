from django_ratelimit.exceptions import Ratelimited

from utils.exceptions import custom_exception_handler


def test_custom_exception_handler_maps_ratelimit_to_429():
    response = custom_exception_handler(Ratelimited(), context={})

    assert response is not None
    assert response.status_code == 429
    assert response.data['detail'] == 'Trop de requetes. Reessayez plus tard.'
