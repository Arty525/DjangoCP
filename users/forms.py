from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from config.settings import EMAIL_HOST_USER
from .models import CustomUser

# Форма регистрации
class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['email', 'username', 'password1', 'password2' ]
        labels = {'email' : 'E-mail',
                  'username' : 'Имя пользователя',
                  'password1' : 'Пароль',
                  'password2' : 'Подтверждение пароля',
                  }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Имя пользователя'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Пароль'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Повторите пароль'})


class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'username']
        REQUIRED_FIELDS = []

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Имя пользователя'})


class CustomUserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Пароль'})

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if not user.is_active:
            raise forms.ValidationError(
                'Ваш email не подтвержден. Пожалуйста, проверьте вашу почту.',
                code='email_not_verified',
            )
        if user.is_banned:
            raise forms.ValidationError(
                'Ваша учетная запись заблокирована.',
                code='banned',
            )


class PasswordRecoveryRequestForm(forms.Form):
    email = forms.EmailField()
    class Meta:
        model = CustomUser
        fields = ['email']
        REQUIRED_FIELDS = []

    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = CustomUser.objects.get(email=email)
        except:
            raise forms.ValidationError('Пользователя с таким email не существует')
        return email


class PasswordChangeForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)

        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Новый пароль'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Новый пароль'})
