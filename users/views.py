from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import LogoutView, LoginView
from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404
from django.urls import  reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, FormView

from config.settings import EMAIL_HOST_USER
from .forms import CustomUserCreationForm, CustomUserUpdateForm, PasswordRecoveryRequestForm, PasswordChangeForm
from .models import CustomUser
from sender.services import UserStatistic


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
    def get_context_data(self, **kwargs):
        statistic = UserStatistic.get_user_statistic(kwargs['pk'])
        context = {
            'success_attempts': statistic[0],
            'fail_attempts': statistic[1],
            'sent_messages': statistic[2],
        }
        return context
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
        user.is_active = True
        user.save()
        return redirect(reverse_lazy('users:success_verify'))

class SuccessVerifyView(TemplateView):
    template_name = 'users/success_verify.html'


class PasswordRecoveryRequestView(FormView):
    model = CustomUser
    template_name = 'users/password_recovery_request.html'
    form_class = PasswordRecoveryRequestForm
    success_url = reverse_lazy('users:password_recovery_request_success')

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        user_pk = get_object_or_404(CustomUser, email=email)
        recovery_url = reverse_lazy('users:password_change', kwargs={'pk': user_pk.pk})
        absolute_url = self.request.build_absolute_uri(recovery_url)

        send_mail(
            subject="Восстановление пароля",
            message=f"Для восстановления пароля пройдите по ссылке:\n{absolute_url}\nЕсли вы не запрашивали восстановление пароля, то проигнорируйте это письмо",
            from_email=EMAIL_HOST_USER,
            recipient_list=[email],
        )
        return redirect(reverse_lazy('users:password_recovery_request_success'))


class PassRecoveryRequsetSuccess(TemplateView):
    template_name = 'users/password_recovery_request_success.html'


class PasswordChangeView(FormView):
    model = CustomUser
    template_name = 'users/password_recovery.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('users:login')
    def post(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, pk=kwargs['pk'])
        print(user.email)
        user.set_password(request.POST.get('password1'))
        user.save()
        update_session_auth_hash(request, user)
        return redirect(reverse_lazy('users:login'))