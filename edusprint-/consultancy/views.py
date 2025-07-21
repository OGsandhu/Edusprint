from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Consultant, ConsultancySlot, Booking
from .serializers import ConsultantSerializer, ConsultancySlotSerializer, BookingSerializer
from django.utils import timezone

# Create your views here.

class ConsultantListView(generics.ListAPIView):
    queryset = Consultant.objects.all()
    serializer_class = ConsultantSerializer
    permission_classes = [permissions.AllowAny]

class AvailableSlotsView(generics.ListAPIView):
    serializer_class = ConsultancySlotSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        now = timezone.now()
        return ConsultancySlot.objects.filter(is_booked=False, start_time__gte=now)

class BookSlotView(generics.CreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        slot_id = request.data.get('slot_id')
        notes = request.data.get('notes', '')
        try:
            slot = ConsultancySlot.objects.get(id=slot_id, is_booked=False)
        except ConsultancySlot.DoesNotExist:
            return Response({'error': 'Slot not available.'}, status=status.HTTP_400_BAD_REQUEST)
        slot.is_booked = True
        slot.save()
        booking = Booking.objects.create(slot=slot, user=request.user, notes=notes)
        serializer = self.get_serializer(booking)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
