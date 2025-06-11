from django import forms
from django.core.exceptions import ValidationError
import os
from .models import Recipient, Message, MailingList

class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = '__all__'

        def __init__(self):
            super(RecipientForm, self).__init__()
            self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})
            self.fields['full_name'].widgets.attrs.update({'class': 'form-control', 'placeholder': 'Full Name'})


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'

        def __init__(self):
            super(RecipientForm, self).__init__()
            self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Title'})
            self.fields['body'].widgets.attrs.update({'class': 'form-control', 'placeholder': 'Text'})


class MailingListForm(forms.ModelForm):
    class Meta:
        model = MailingList
        fields = '__all__'

        def __init__(self):
            super(RecipientForm, self).__init__()
            self.fields['status'].widget.attrs.update({'class': 'dropdown', 'placeholder': 'Status'})
            self.fields['message'].widgets.attrs.update({'class': 'dropdown', 'placeholder': 'Message'})
            self.fields['recipients'].widgets.attrs.update({'class': 'form-check', 'placeholder': 'Recipients'})