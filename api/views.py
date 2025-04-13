# from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse, HttpResponse
import os
from django.conf import settings


def index(request):
    return HttpResponse("Homepage. Please use the app from the frontend")


@api_view(["POST"])
def register(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"})
    user = User.objects.create_user(username=username, password=password)
    return Response({"success": True})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def addpdf(request):
    upload_dir = settings.MEDIA_ROOT
    os.makedirs(upload_dir, exist_ok=True)
    if request.method == "POST":
        for f in request.FILES.getlist("files"):
            file_path = os.path.join(upload_dir, f.name)
            with open(file_path, "wb+") as dest:
                for chunk in f.chunks():
                    dest.write(chunk)
        return JsonResponse({"ok": True})


# @api_view(["POST"])
# def addpdf(request):
#     auth = JWTAuthentication()
#     validated = auth.authenticate(request)
#     print("JWT manually authenticated:", validated)
#     return JsonResponse({"ok": True})


def addapi(request):
    api_key = request.GET.get("api_key")

    if not api_key:
        return JsonResponse({"valid": False}, status=400)

    if api_key == "test1":
        return JsonResponse({"valid": True})
    else:
        return JsonResponse({"valid": False})


def ask(request):
    question = request.GET.get("question")

    if not question:
        return JsonResponse({}, status=400)
    answer = "Answer of the question, " + question
    return JsonResponse({"answer": answer})
