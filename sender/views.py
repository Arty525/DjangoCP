import json
from urllib import request

from django.http import HttpResponse
from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, TemplateView, DetailView, DeleteView

from .forms import RecipientForm, MessageForm, MailingListForm
from .models import Recipient, Message, MailingList, SendAttempt
# Create your views here.

class MailingListView(ListView):
    model = MailingList
    template_name = 'sender/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        active_mailing_lists = MailingList.objects.filter(status='started')
        mailing_lists = MailingList.objects.all()
        unique_recipients = Recipient.objects.all()
        context = {
            'mailing_lists': mailing_lists.count(),
            'active_mailing_lists': active_mailing_lists.count(),
            'unique_recipients': unique_recipients.count()
        }
        return context


class RecipientCreateView(CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'sender/recipients/add.html'

    def get_success_url(self):
        return reverse_lazy('sender:index')


class RecipientUpdateView(UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'sender/recipients/update.html'

    def get_success_url(self):
        return reverse_lazy('sender:index')


class RecipientListView(ListView):
    model = Recipient
    template_name = 'sender/recipients/list.html'
    context_object_name = 'recipients'


class RecipientView(DetailView):
    model = Recipient
    template_name = 'sender/recipients/recipient.html'
    context_object_name = 'recipient'


class RecipientDeleteView(DeleteView):
    model = Recipient
    template_name = 'sender/recipients/delete.html'
    success_url = reverse_lazy('sender:index')


class MessageCreateView(CreateView):
    model = Message
    template_name = 'sender/message/add.html'
    form_class = MessageForm
    def get_success_url(self):
        return reverse_lazy('sender:message', kwargs={'pk': self.object.pk})


class MessageUpdateView(UpdateView):
    model = Message
    template_name = 'sender/message/update.html'
    form_class = MessageForm
    def get_success_url(self):
        return reverse_lazy('sender:message', kwargs={'pk': self.object.pk})


class MessageListView(ListView):
    model = Message
    template_name = 'sender/message/list.html'
    context_object_name = 'messages'


class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'sender/message/delete.html'
    success_url = reverse_lazy('sender:messages_list')


class MessageDetailView(DetailView):
    model = Message
    template_name = 'sender/message/message.html'
    context_object_name = 'message'


class MailingListCreateView(CreateView):
    model = MailingList
    template_name = 'sender/mailing_list/add.html'
    form_class = MailingListForm
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('sender:mailing_list', kwargs={'pk': self.object.pk})

class MailingListUpdateView(UpdateView):
    model = MailingList
    template_name = 'sender/mailing_list/update.html'
    form_class = MailingListForm
    def get_success_url(self):
        return reverse_lazy('sender:mailing_list', kwargs={'pk': self.object.pk})


class MailingListDeleteView(DeleteView):
    model = MailingList
    template_name = 'sender/mailing_list/delete.html'
    success_url = reverse_lazy('sender:mailing_lists')


class MailingListDetailView(DetailView):
    model = MailingList
    template_name = 'sender/mailing_list/mailing_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        mailing_list = MailingList.objects.get(pk=self.object.pk)
        recipients = mailing_list.recipients.all()
        context = {
            'mailing_list': mailing_list,
            'recipients': recipients
        }
        return context


class MailingListsListView(ListView):
    model = MailingList
    template_name = 'sender/mailing_list/list.html'
    context_object_name = 'mailing_lists'


class RunSend(View):
    success_url = reverse_lazy('sender:mailing_lists')
    def post(self, request, *args, **kwargs):
        mailing_list = get_object_or_404(MailingList, id=self.kwargs['pk'])
        result = mailing_list.send()
        return redirect(self.success_url)


