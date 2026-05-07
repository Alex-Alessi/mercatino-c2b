from django.urls import path
from .views import (
    dashboard_view,
    proposal_create_view,
    proposal_detail_view,
)

urlpatterns = [
    path("", dashboard_view, name="dashboard"),
    path("proposte/nuova/", proposal_create_view, name="proposal_create"),
    path("proposte/<int:pk>/", proposal_detail_view, name="proposal_detail"),
]