from rest_framework import serializers
from .models import Consultant, ConsultancySlot, Booking

class ConsultantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultant
        fields = ['id', 'user', 'bio', 'expertise']

class ConsultancySlotSerializer(serializers.ModelSerializer):
    consultant = ConsultantSerializer(read_only=True)
    class Meta:
        model = ConsultancySlot
        fields = ['id', 'consultant', 'start_time', 'end_time', 'is_booked']

class BookingSerializer(serializers.ModelSerializer):
    slot = ConsultancySlotSerializer(read_only=True)
    class Meta:
        model = Booking
        fields = ['id', 'slot', 'user', 'booked_at', 'notes'] 