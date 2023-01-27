import jwt
from django.conf.global_settings import SECRET_KEY
from django.contrib.auth.models import User
from django.http import JsonResponse


# decorator to check if token is valid, and put the user in the request
def token_required(view_func):
    def wrapper(request, *args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return JsonResponse({"message": "Missing token"}, status=401)
        try:
            payload = jwt.decode(token, key=SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return JsonResponse({"message": "Token expired"}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"message": "Invalid token"}, status=401)
        user = User.objects.get(username=payload["username"])
        request.auth_user = user
        return view_func(request, *args, **kwargs)

    return wrapper
