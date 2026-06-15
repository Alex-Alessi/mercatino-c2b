from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import register_view, privacy_policy_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("registrati/", register_view, name="register"),
    path("login/", LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("privacy/", privacy_policy_view, name="privacy_policy"),
    path("password-reset/", 
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset.html",
        ), 
        name="password_reset",
    ),
    path("password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path(
        "password-change/",
        auth_views.PasswordChangeView.as_view(
            template_name="accounts/password_change.html"
        ),
        name="password_change",
    ),

    path(
        "password-change_done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="accounts/password_change_done.html"
        ),
        name="password_change_done",
    ),
]