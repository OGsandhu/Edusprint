from django.urls import path
from .views import ConsultantListView, AvailableSlotsView, BookSlotView

urlpatterns = [
    path('consultants/', ConsultantListView.as_view(), name='consultant-list'),
    path('slots/', AvailableSlotsView.as_view(), name='available-slots'),
    path('book/', BookSlotView.as_view(), name='book-slot'),
] 