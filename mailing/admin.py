from django.contrib import admin
from .models import Message, Campaign


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "topic",
    )
    search_fields = ("topic",)


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "status",
    )
    search_fields = ("status",)