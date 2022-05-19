from common.tokens import AuthBackend
from user.models import User


class DisableCSRFForAPI(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        setattr(request, "_dont_enforce_csrf_checks", True)
        response = self.get_response(request)
        return response


def get_token(request):
    """Get token from HTTP header"""
    if "HTTP_AUTHORIZATION" in request.META:

        full_auth = request.META["HTTP_AUTHORIZATION"].split(" ")
        if len(full_auth) < 2 or full_auth[0] != "Token":
            return None
        token = full_auth[1].strip('"')

        return token
    return None


class AuthAPI(object):
    """
    Add user to request var for API calls

    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = get_token(request)
        if token:
            user_email = AuthBackend.authenticate(request, token=token)
            try:
                user = User.objects.get(email=user_email)
            except User.DoesNotExist:
                user = None

            if user:
                user.backend = "common.tokens.AuthBackend"
                request.user = user
                request.auth = True

        return self.get_response(request)
