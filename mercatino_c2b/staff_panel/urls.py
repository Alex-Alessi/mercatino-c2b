from django.urls import path
from .views import staff_proposal_list_view, staff_proposal_detail_view

urlpatterns = [
    path('proposte/', staff_proposal_list_view, name="staff_proposal_list"),
    path('proposte/<int:pk>/', staff_proposal_detail_view, name="staff_proposal_detail")
]