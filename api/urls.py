from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [  # simple, naming,
    path("", views.index, name="index"),
    path("addapi/", views.addapi, name="addapi"),
    path("ask/", views.ask, name="ask"),
    path("test1/", views.test1, name="test1"),
    path("addpdf/", views.addpdf, name="addpdf"),
    path("getpdf/", views.getpdf, name="getpdf"),
    path("removepdf/", views.removepdf, name="removepdf"),
    path("register/", views.register, name="register"),
    # path("login/", views.login, name="login"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
