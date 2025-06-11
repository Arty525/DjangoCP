from django.db import models

# Create your models here.

class Recipient(models.Model):
    email = models.EmailField(verbose_name='Email', unique=True)
    full_name = models.CharField(verbose_name='Ф. И. О.')
    comment = models.TextField(verbose_name='Комментарий')

    def __str__(self):
        return f'{self.email} - {self.full_name}'

    class Meta:
        verbose_name = 'Получатель'
        verbose_name_plural = 'Получатели'
        ordering = ['email']

class Message(models.Model):
    title = models.CharField(verbose_name='Тема письма', max_length=255)
    body = models.TextField(verbose_name='Тело письма')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['title']

class MailingList(models.Model):
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('complited', 'Завершена'),
    ]

    date_first_sent = models.DateField(verbose_name='Дата первой отправки', auto_now_add=True)
    date_last_sent = models.DateField(verbose_name='Дата последней отправки', auto_now=True)
    status = models.CharField(verbose_name='Статус', choices=STATUS_CHOICES, max_length=10, default='created')
    message = models.ForeignKey(Message, verbose_name='Сообщение', on_delete=models.CASCADE)
    recipients = models.ManyToManyField(Recipient, verbose_name='Получатели')


class SendAttempt(models.Model):
    date = models.DateField(verbose_name='Дата', auto_now_add=True)
    status = models.CharField(verbose_name='Статус', max_length=50)
    response = models.TextField(verbose_name='Ответ сервера')
    mailing_list = models.ForeignKey(MailingList, verbose_name='Рассылка', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Состояние рассылки'
        verbose_name_plural = 'Состояния рассылок'
        ordering = ['status', 'date']


