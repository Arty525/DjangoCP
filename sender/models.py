from django.db import models

# Create your models here.

class Recipient(models.Model):
    email = models.EmailField(verbose_name='Email', unique=True)
    full_name = models.CharField(verbose_name='Full Name')
    comment = models.TextField(verbose_name='Comment')

    def __str__(self):
        return f'{self.email} - {self.full_name}'

    class Meta:
        verbose_name = 'Recipient'
        verbose_name_plural = 'Recipients'
        ordering = ['email']

class Message(models.Model):
    title = models.CharField(verbose_name='Title', max_length=255)
    body = models.TextField(verbose_name='Body')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['title']

class MailingList(models.Model):
    date_first_sent = models.DateField(verbose_name='Date First Sent', auto_now_add=True)
    date_last_sent = models.DateField(verbose_name='Date Last Sent', auto_now=True)
    status = models.CharField(verbose_name='Status')
    message = models.ForeignKey(Message, verbose_name='Message', on_delete=models.CASCADE)
    recipients = models.ManyToManyField(Recipient, verbose_name='Recipients')


class SendAttempt(models.Model):
    date = models.DateField(verbose_name='Date', auto_now_add=True)
    status = models.CharField(verbose_name='Status', max_length=50)
    response = models.TextField(verbose_name='Response')
    mailing_list = models.ForeignKey(MailingList, verbose_name='Mailing List', on_delete=models.CASCADE)


