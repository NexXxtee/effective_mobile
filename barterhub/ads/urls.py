from django.urls import path
from .views import AdCreateView, AdDeleteView, AdDetailView, AdListView, AdUpdateView, ProfileView, ExchangeProposalCreateView, ExchangeProposalStatusView

app_name = 'ads'

urlpatterns = [
    path('', AdListView.as_view(), name='ad_list'),
    path('ad/<int:pk>/', AdDetailView.as_view(), name='ad_detail'),
    path('ad/create/', AdCreateView.as_view(), name='ad_create'),
    path('ad/<int:pk>/edit/', AdUpdateView.as_view(), name='ad_edit'),
    path('ad/<int:pk>/delete/', AdDeleteView.as_view(), name='ad_delete'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('ad/<int:pk>/exchange/', ExchangeProposalCreateView.as_view(), name='exchange_proposal_create'),
    path('proposal/<int:pk>/status/', ExchangeProposalStatusView.as_view(), name='proposal_status'),
]