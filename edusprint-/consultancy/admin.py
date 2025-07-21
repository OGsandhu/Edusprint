from django.contrib import admin
from .models import Consultant, ConsultancySlot, Booking

# Register your models here.
admin.site.register(Consultant)
admin.site.register(ConsultancySlot)
admin.site.register(Booking)
