import json
from datetime import datetime, timedelta

import jwt
from django.conf.global_settings import SECRET_KEY
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods


# Create your views here.
# json endpoint to register a user
# POST /api/auth/register/
@require_http_methods(["POST"])
def register_view(request):
    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")
    if username and password:
        new_user = User.objects.create_user(username=username, password=password)
        return JsonResponse(
            {"message": "Registration successful",
             "username": new_user.username},
            status=201)
    return JsonResponse({"message": "Registration failed"}, status=400)

# view to login a user using jwt token
@require_http_methods(["POST"])
def login_view(request):
    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")
    user = authenticate(username=username, password=password)
    if not user:
        return JsonResponse({"message": "Invalid credentials"}, status=401)
    token = jwt.encode(
        {"username": user.username, "exp": datetime.now() + timedelta(days=1)},
        key = SECRET_KEY,
        algorithm="HS256"
    )
    return JsonResponse({"token": token}, status=200)

