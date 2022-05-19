from django.http import JsonResponse


def auth_required(func):
    def wrap(request, *args, **kwargs):
        error401 = JsonResponse({"error": "Please authenticate "}, status=401)
        if "HTTP_AUTHORIZATION" in request.META:
            if request.user is None or request.user.is_anonymous:
                return error401
            else:
                return func(request, *args, **kwargs)
        else:
            return error401

    return wrap
