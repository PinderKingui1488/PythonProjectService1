from django.forms import ModelForm
from mailing.models import Message, Campaign


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        self.fields["topic"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Тема письма"}
        )

        self.fields["body"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Содержание"}
        )


class CampaignForm(ModelForm):
    class Meta:
        model = Campaign
        fields = ["first_sent_time", "end_time", "status", "message", "is_active", "recipients",
                  "successful_attempts", "unsuccessful_attempts", "sent_messages"]

    def __init__(self, *args, **kwargs):
        super(CampaignForm, self).__init__(*args, **kwargs)

        self.fields["message"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Сообщение"}
        )

        self.fields["recipients"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Получатели"}
        )


class CampaignModeratorForm(ModelForm):
    class Meta:
        model = Campaign
        fields = ["is_active"]