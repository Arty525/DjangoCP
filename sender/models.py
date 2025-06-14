import os
import smtplib

from django.contrib.auth import user_logged_in
from django.core.mail import send_mail
from django.db import models
from users.models import CustomUser

from config import settings


# Create your models here.

class Recipient(models.Model):
    email = models.EmailField(verbose_name='Email', unique=True)
    full_name = models.CharField(verbose_name='Ф. И. О.')
    comment = models.TextField(verbose_name='Комментарий')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.email} - {self.full_name}'

    class Meta:
        verbose_name = 'Получатель'
        verbose_name_plural = 'Получатели'
        ordering = ['email']
        permissions = [
            ("can_view_recipient", "Can view recipient"),
        ]

class Message(models.Model):
    title = models.CharField(verbose_name='Тема письма', max_length=255)
    body = models.TextField(verbose_name='Тело письма')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['title']
        permissions = [
            ("can_view_message", "Can view message"),
        ]

class MailingList(models.Model):
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('completed', 'Завершена'),
    ]

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        permissions = [
            ("can_view_mailing_list", "Can view mailing list"),
            ("can_turn_off", "Can turn off mailing list"),
        ]

    date_first_sent = models.DateTimeField(verbose_name='Дата первой отправки', auto_now_add=True)
    date_last_sent = models.DateTimeField(verbose_name='Дата последней отправки', auto_now=True)
    status = models.CharField(verbose_name='Статус', choices=STATUS_CHOICES, max_length=10, default='created')
    message = models.ForeignKey(Message, verbose_name='Сообщение', on_delete=models.CASCADE)
    recipients = models.ManyToManyField(Recipient, verbose_name='Получатели')
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)

    def send(self):
        if not self.is_active:
            raise
        self.status = 'started'
        self.save()

        subject = self.message.title
        message = self.message.body
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [r.email for r in self.recipients.all()]

        try:
            # Отправка писем
            success_count = send_mail(
                subject,
                message,
                from_email,
                recipient_list,
                fail_silently=False,
            )

            # Логирование результата
            self.status = 'completed'
            self.save()

            SendAttempt.objects.create(
                mailing_list=self,
                status='Успешно',
                response=f"Письма успешно отправлены",
                user=self.user,
            )

            return success_count

        except smtplib.SMTPException as e:
            self.status = 'completed'
            self.save()

            SendAttempt.objects.create(
                mailing_list=self,
                status='Не успешно',
                response=f"SMTP ошибка: {str(e)}",
                user=self.user,
            )
            raise

        except Exception as e:
            self.status = 'completed'
            self.save()

            SendAttempt.objects.create(
                mailing_list=self,
                status='Не успешно',
                response=f"Неизвестная ошибка: {str(e)}",
                user=self.user,
            )
            raise


class SendAttempt(models.Model):
    date = models.DateTimeField(verbose_name='Дата', auto_now_add=True)
    status = models.CharField(verbose_name='Статус', max_length=50)
    response = models.TextField(verbose_name='Ответ сервера')
    mailing_list = models.ForeignKey(MailingList, verbose_name='Рассылка', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Состояние рассылки'
        verbose_name_plural = 'Состояния рассылок'
        ordering = ['status', 'date']
