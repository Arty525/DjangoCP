from django.contrib.auth.views import LogoutView
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import  reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from config.settings import EMAIL_HOST_USER
from .forms import CustomUserCreationForm, CustomUserUpdateForm
from .models import CustomUser


class RegistrationView(CreateView):
    model = CustomUser
    template_name='users/registration.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        verification_url = reverse_lazy('users:verify_email', kwargs={'pk': user.pk})
        absolute_url = self.request.build_absolute_uri(verification_url)
        email = form.cleaned_data.get('email')
        send_mail(
            subject="Регистрация на сайте",
            message=f"Здравствуйте!\nВы зарегистрировались на сайте.\nДля подтверждения email перейдите по ссылке:\n{absolute_url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[email],
        )
        return super().form_valid(form)

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('sender:index')

class ProfileView(TemplateView):
    template_name = 'users/profile.html'

class ProfileUpdateView(UpdateView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    def get_success_url(self):
        return reverse_lazy('users:profile', kwargs={'pk': self.object.pk})
    template_name = 'users/update.html'


class VerifyEmailView(View):
    def get(self, request, *args, **kwargs):
        user = CustomUser.objects.get(pk=self.kwargs['pk'])
        user.email_verified = True
        user.save()
        return redirect(reverse_lazy('users:success_verify'))

class SuccessVerifyView(TemplateView):
    template_name = 'users/success_verify.html'