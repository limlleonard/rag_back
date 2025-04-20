# from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status

# from rest_framework.views import APIView
from django.http import JsonResponse, HttpResponse
from django.conf import settings
import os
from .llm import Agent

agent1 = Agent()  # later dictionary to separate users


def rmdir1(dir1):
    if os.path.isdir(dir1):
        for f in os.listdir(dir1):
            file_path = os.path.join(dir1, f)
            os.remove(file_path)
        os.rmdir(dir1)


def index(request):
    return HttpResponse("Homepage. Please use the app from the frontend")


@api_view(["POST"])
def register(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if User.objects.filter(username=username).exists():
        return Response(status=403)
    user = User.objects.create_user(username=username, password=password)
    return Response()


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def addpdf(request):
    username = request.user.username
    dir_pdf = os.path.join(settings.MEDIA_ROOT, username)
    dir_vec = os.path.join(settings.MEDIA_ROOT, username + "_vec")
    os.makedirs(dir_pdf, exist_ok=True)
    lst_added = []
    lst_conflict = []
    for f in request.FILES.getlist("files"):
        file_path = os.path.join(dir_pdf, f.name)
        if os.path.isfile(file_path):
            lst_conflict.append(f.name)
        else:
            lst_added.append(file_path)
            with open(file_path, "wb") as w:
                for chunk in f.chunks():
                    w.write(chunk)
    if not os.path.isdir(dir_vec):
        os.makedirs(dir_vec)
        agent1.embed(dir_pdf, dir_vec)
    else:
        agent1.refresh(dir_vec, lst_added)
    return Response({"conflict": lst_conflict})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getpdf(request):
    username = request.user.username
    dir_pdf = os.path.join(settings.MEDIA_ROOT, username)
    base_url = request.build_absolute_uri(settings.MEDIA_URL + f"{username}/")

    files = []
    if os.path.isdir(dir_pdf):
        for filename in os.listdir(dir_pdf):
            if filename.endswith(".pdf"):
                files.append({"name": filename, "url": base_url + filename})
    return Response(files)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def removepdf(request):
    username = request.user.username
    dir_pdf = os.path.join(settings.MEDIA_ROOT, username)
    dir_vec = os.path.join(settings.MEDIA_ROOT, username + "_vec")
    rmdir1(dir_pdf)
    rmdir1(dir_vec)
    return Response()


def addapi(request):
    api_key = request.GET.get("api_key")

    if not api_key:
        return JsonResponse({"valid": False}, status=400)

    if api_key == "test1":
        return JsonResponse({"valid": True})
    else:
        return JsonResponse({"valid": False})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def ask(request):
    """Check if agent1 is initialized."""
    if agent1.index is None:
        username = request.user.username
        dir_vec = os.path.join(settings.MEDIA_ROOT, username + "_vec")
        if os.path.isdir(dir_vec):
            agent1.reload_index(dir_vec)
        else:
            return Response({"answer": "Please upload PDF files first"}, status=400)
    question = request.GET.get("question")
    if not question:
        return Response({}, status=400)
    # answer = "Answer of the question, " + question
    context = agent1.qa(question)
    return Response(context)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def test1(request):
    user = request.user
    dir_pdf = os.path.join(settings.MEDIA_ROOT, user.username)
    agent1.init_llama()
    agent1.embed(dir_pdf)
    return Response()


# class GetPDFsView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         folder_path = os.path.join(settings.MEDIA_ROOT, "pdfs")
#         base_url = request.build_absolute_uri(settings.MEDIA_URL + "pdfs/")

#         files = []
#         for filename in os.listdir(folder_path):
#             if filename.endswith(".pdf"):
#                 files.append({
#                     "name": filename,
#                     "url": base_url + filename
#                 })

#         return Response(files)
