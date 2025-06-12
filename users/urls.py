from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import RegisterView, LogoutView, ProfileView, ProfileUpdateView, VerifyEmailView

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='sender:index'), name='logout'),
    path('registrations/', RegisterView.as_view(template_name='users/registration.html'), name='registration'),
    path('profile/<int:pk>', ProfileView.as_view(), name='profile'),
    path('update/<int:pk>', ProfileUpdateView.as_view(), name='update'),
    path('verify_email/<int:pk>', VerifyEmailView.as_view(), name='verify_email'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)