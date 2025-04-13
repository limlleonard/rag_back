# from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def csrf(request):
    return JsonResponse({"ok": True})


def index(request):
    return HttpResponse("Homepage. Please use the app from the frontend")


def addpdf(request):
    if request.method == "POST":
        for f in request.FILES.getlist("files"):
            with open(f"media/uploads/{f.name}", "wb+") as dest:
                for chunk in f.chunks():
                    dest.write(chunk)
        return JsonResponse({"ok": True})


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
