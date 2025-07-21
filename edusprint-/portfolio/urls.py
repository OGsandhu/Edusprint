from django.urls import path
from .views import PortfolioListCreateView, PortfolioDeleteView

urlpatterns = [
    path('', PortfolioListCreateView.as_view(), name='portfolio-list-create'),
    path('<int:pk>/', PortfolioDeleteView.as_view(), name='portfolio-delete'),
]
