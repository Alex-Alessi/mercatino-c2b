from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import register_view, privacy_policy_view

urlpatterns = [
    path("registrati/", register_view, name="register"),
    path("login/", LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("privacy/", privacy_policy_view, name="privacy_policy")
]