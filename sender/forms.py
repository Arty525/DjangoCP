from django import forms
from .models import Recipient, Message, MailingList


class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ["email", "full_name", "comment"]

        def __init__(self):
            super(RecipientForm, self).__init__()
            self.fields["email"].widget.attrs.update(
                {"class": "form-control", "placeholder": "Email"}
            )
            self.fields["full_name"].widgets.attrs.update(
                {"class": "form-control", "placeholder": "Ф. И. О."}
            )
            self.fields["comment"].widgets.attrs.update(
                {"class": "form-control", "placeholder": "Комментарий"}
            )


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["title", "body"]

        def __init__(self):
            super(RecipientForm, self).__init__()
            self.fields["title"].widget.attrs.update(
                {"class": "form-control", "placeholder": "Title"}
            )
            self.fields["body"].widgets.attrs.update(
                {"class": "form-control", "placeholder": "Text"}
            )


class MailingListForm(forms.ModelForm):
    class Meta:
        model = MailingList
        fields = ["message", "recipients"]

        def __init__(self):
            super(RecipientForm, self).__init__()
            self.fields["message"].widgets.attrs.update(
                {"class": "dropdown", "placeholder": "Message"}
            )
            self.fields["recipients"].widgets.attrs.update(
                {"class": "form-check", "placeholder": "Recipients"}
            )
