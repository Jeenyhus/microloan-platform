import json
from .models import AuditLog

class AuditLogMiddleware:
    """
    AuditLogMiddleware class for logging API requests and responses.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if request.user.is_authenticated and request.path.startswith('/api/'):
            AuditLog.objects.create(
                user=request.user,
                company=request.user.company,
                action=f"{request.method} {request.path}",
                details={
                    'method': request.method,
                    'path': request.path,
                    'status_code': response.status_code,
                    'data': json.loads(request.body.decode('utf-8')) if request.body else None
                }
            )
        
        return response
