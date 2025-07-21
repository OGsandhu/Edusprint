from django.db import models
from django.conf import settings

class Consultant(models.Model):
    """A consultant who can offer consultancy slots."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    expertise = models.CharField(max_length=255)

    def __str__(self):
        # Fallback if get_full_name is not implemented
        if hasattr(self.user, 'get_full_name'):  # type: ignore
            name = self.user.get_full_name()  # type: ignore
            if name:
                return name
        return str(self.user)

class ConsultancySlot(models.Model):
    """A time slot offered by a consultant for booking."""
    consultant = models.ForeignKey(Consultant, on_delete=models.CASCADE, related_name='slots')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_booked = models.BooleanField(default=False)  # type: ignore

    def __str__(self):
        return f"{self.consultant} | {self.start_time} - {self.end_time}"

class Booking(models.Model):
    """A booking made by a user for a consultancy slot."""
    slot = models.OneToOneField(ConsultancySlot, on_delete=models.CASCADE, related_name='booking')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user} booked {self.slot}"
