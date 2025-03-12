from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.views import (
    MessageListView,
    MessageDeleteView,
    MessageDetailView,
    MessageUpdateView,
    MessageCreateView,
    CampaignCreateView,
    CampaignDeleteView,
    CampaignDetailView,
    CampaignUpdateView,
    CampaignListView,
)

app_name = "mailing"

urlpatterns = [
    path("message/list", cache_page(60)(MessageListView.as_view()), name="message_list"),
    path("message/detail/<int:pk>", cache_page(60)(MessageDetailView.as_view()), name="message_detail"),
    path("message/delete/<int:pk>", MessageDeleteView.as_view(), name="message_delete"),
    path("message/create", MessageCreateView.as_view(), name="message_create"),
    path("message/update/<int:pk>", MessageUpdateView.as_view(), name="message_update"),
    path("campaign/list", cache_page(60)(CampaignListView.as_view()), name="campaign_list"),
    path("campaign/detail/<int:pk>", cache_page(60)(CampaignDetailView.as_view()), name="campaign_detail"),
    path("campaign/delete/<int:pk>", CampaignDeleteView.as_view(), name="campaign_delete"),
    path("campaign/create", CampaignCreateView.as_view(), name="campaign_create"),
    path("campaign/update/<int:pk>", CampaignUpdateView.as_view(), name="campaign_update"),
]