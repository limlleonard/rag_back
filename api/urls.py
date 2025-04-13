from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("addapi/", views.addapi, name="addapi"),
    path("ask/", views.ask, name="ask"),
    path("addpdf/", views.addpdf, name="addpdf"),
    path("csrf/", views.csrf, name="csrf"),
]
