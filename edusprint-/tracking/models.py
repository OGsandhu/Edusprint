from django.db import models
from django.conf import settings

# Create your models here.

class RequestLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    path = models.CharField(max_length=512)
    method = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)
    remote_addr = models.GenericIPAddressField(null=True, blank=True)
    query_params = models.TextField(blank=True)
    body = models.TextField(blank=True)

    def __str__(self):
        return f"{self.method} {self.path} at {self.timestamp}"
