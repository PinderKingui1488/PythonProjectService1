from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from mailing.forms import MessageForm, CampaignForm
from mailing.models import Message, Campaign
from mailing.services import get_campaign_from_cache


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailings:message_list")


class MessageListView(ListView):
    model = Message
    template_name = "mailings/message_list.html"


class MessageDetailView(DetailView):
    model = Message


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailings:message_list")


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy("mailings:message_list")


class CampaignCreateView(LoginRequiredMixin, CreateView):
    model = Campaign
    form_class = CampaignForm
    success_url = reverse_lazy("mailings:campaign_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CampaignListView(LoginRequiredMixin, ListView):
    model = Campaign
    template_name = "mailings/campaign_list.html"

    def get_queryset(self):
        if self.request.user.is_staff:
            return get_campaign_from_cache()
        return Campaign.objects.filter(owner=self.request.user)


class CampaignDetailView(LoginRequiredMixin, DetailView):
    model = Campaign

    def get_queryset(self):
        if self.request.user.is_staff:
            return Campaign.objects.all()
        return Campaign.objects.filter(owner=self.request.user)


class CampaignUpdateView(LoginRequiredMixin, UpdateView):
    model = Campaign
    form_class = CampaignForm
    success_url = reverse_lazy("mailings:campaign_list")

    def get_queryset(self):
        if self.request.user.is_staff:
            return Campaign.objects.all()
        return Campaign.objects.filter(owner=self.request.user)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'toggle_active' in request.POST:
            self.object.is_active = not self.object.is_active
            self.object.save()
            return redirect(self.success_url)
        return super().post(request, *args, **kwargs)


class CampaignDeleteView(LoginRequiredMixin, DeleteView):
    model = Campaign
    success_url = reverse_lazy("mailings:campaign_list")

    def get_queryset(self):
        if self.request.user.is_staff:
            return Campaign.objects.all()
        return Campaign.objects.filter(owner=self.request.user)