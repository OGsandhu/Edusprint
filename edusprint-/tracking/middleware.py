"""Middleware for logging each request to the RequestLog model."""
from .models import RequestLog
from django.utils.deprecation import MiddlewareMixin

# Logs every incoming request to the database
class RequestLogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user = request.user if request.user.is_authenticated else None
        path = request.path
        method = request.method
        remote_addr = request.META.get('REMOTE_ADDR')
        query_params = request.META.get('QUERY_STRING', '')
        body = ''
        if method in ['POST', 'PUT', 'PATCH']:
            try:
                body = request.body.decode('utf-8')
            except Exception:
                body = str(request.body)
        RequestLog.objects.create(  # type: ignore
            user=user,
            path=path,
            method=method,
            remote_addr=remote_addr,
            query_params=query_params,
            body=body
        ) 