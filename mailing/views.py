from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from mailing.forms import MessageForm, CampaignForm, CampaignModeratorForm
from mailing.models import Message, Campaign
from mailing.services import get_campaign_from_cache


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")


class MessageListView(ListView):
    model = Message
    template_name = "mailing/message_list.html"


class MessageDetailView(DetailView):
    model = Message


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy("mailing:message_list")


class CampaignCreateView(CreateView):
    model = Campaign
    form_class = CampaignForm
    success_url = reverse_lazy("mailing:campaign_list")

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class CampaignListView(ListView):
    model = Campaign
    template_name = "mailing/campaign_list.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm("mailing.view_campaign"):
            return HttpResponseForbidden(
                "У вас нет прав для просмотра списка рассылок."
            )
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return get_campaign_from_cache()


class CampaignDetailView(DetailView):
    model = Campaign


class CampaignUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Campaign
    form_class = CampaignForm
    success_url = reverse_lazy("mailing:campaign_list")

    permission_required = "mailing.can_disable_mailing"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = not self.object.is_active
        self.object.save()
        return redirect(self.success_url)

    def handle_no_permission(self):
        return HttpResponseForbidden("У вас нет прав для отключения рассылки.")

    def get_form_class(self):
        user = self.request.user
        if user.is_superuser:
            return CampaignForm
        elif user.has_perm("mailing.can_disable_mailing"):
            return CampaignModeratorForm
        else:
            raise PermissionDenied

    def test_func(self):
        user = self.request.user
        obj = self.get_object()
        return user.has_perm("mailing.can_disable_mailing")


class CampaignDeleteView(DeleteView):
    model = Campaign
    success_url = reverse_lazy("mailing:campaign_list")