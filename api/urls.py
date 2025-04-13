from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("addapi/", views.addapi, name="addapi"),
    path("ask/", views.ask, name="ask"),
    path("addpdf/", views.addpdf, name="addpdf"),
    path("register/", views.register, name="register"),
    # path("login/", views.login, name="login"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
