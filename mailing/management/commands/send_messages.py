from django.core.mail import send_mail
from django.core.management import BaseCommand
from django.utils import timezone
from config.settings import EMAIL_HOST_USER
from mailing.models import Campaign, CampaignAttempt


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        mailing = Campaign.objects.filter(status__in=["created", "started"])
        for campaign in mailing:
            for recipient in campaign.recipients.all():
                try:
                    send_mail(
                        campaign.message.topic,
                        campaign.message.body,
                        from_email=EMAIL_HOST_USER,
                        recipient_list=[recipient.email],
                        fail_silently=False,
                    )
                    CampaignAttempt.objects.create(
                        date_attempt=timezone.now(),
                        status="status_ok",
                        server_response="Email отправлен",
                        campaign=campaign,
                    )
                    print(
                        f"Сообщение {campaign.message.topic} отправлено на {recipient.email}."
                    )
                except Exception as e:
                    CampaignAttempt.objects.create(
                        date_attempt=timezone.now(),
                        status="status_nok",
                        server_response=str(e),
                        campaign=campaign,
                    )
                    print(str(e))
            campaign.save()