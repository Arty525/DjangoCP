from django.contrib.auth.views import LoginView
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    RegistrationView,
    LogoutView,
    ProfileView,
    ProfileUpdateView,
    VerifyEmailView,
    SuccessVerifyView,
    PasswordChangeView,
    PasswordRecoveryRequestView,
    PassRecoveryRequsetSuccess,
    UserListView,
    ChangeUserStatus,
)

app_name = "users"

urlpatterns = [
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="sender:index"), name="logout"),
    path(
        "registrations/",
        RegistrationView.as_view(template_name="users/registration.html"),
        name="registration",
    ),
    path("profile/<int:pk>", ProfileView.as_view(), name="profile"),
    path("update/<int:pk>", ProfileUpdateView.as_view(), name="update"),
    path("verify_email/<int:pk>/", VerifyEmailView.as_view(), name="verify_email"),
    path("success_verify/", SuccessVerifyView.as_view(), name="success_verify"),
    path(
        "password_recovery_request/",
        PasswordRecoveryRequestView.as_view(),
        name="password_recovery_request",
    ),
    path(
        "password_recovery_request_success/",
        PassRecoveryRequsetSuccess.as_view(),
        name="password_recovery_request_success",
    ),
    path(
        "password_change/<int:pk>/",
        PasswordChangeView.as_view(),
        name="password_change",
    ),
    path("user_list/", UserListView.as_view(), name="user_list"),
    path("ban_user/<int:pk>", ChangeUserStatus.as_view(), name="ban_user"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
