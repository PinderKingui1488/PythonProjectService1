from django.urls import path
from django.views.decorators.cache import cache_page

from clients.views import (
    ClientsListView,
    HomeView,
    ClientsDetailView,
    ClientsDeleteView,
    ClientsCreateView,
    ClientsUpdateView,
)

app_name = "clients"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("clients/list", cache_page(60)(ClientsListView.as_view()), name="clients_list"),
    path("clients/detail/<int:pk>", cache_page(60)(ClientsDetailView.as_view()), name="clients_detail"),
    path("clients/delete/<int:pk>", ClientsDeleteView.as_view(), name="clients_delete"),
    path("clients/create", ClientsCreateView.as_view(), name="clients_create"),
    path("clients/update/<int:pk>", ClientsUpdateView.as_view(), name="clients_update"),
]