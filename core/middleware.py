
import json
from .models import PlatformApiCall
from django.utils.deprecation import MiddlewareMixin

class ApiAuditMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        try:
            user = getattr(request, 'user', None)
            PlatformApiCall.objects.create(
                user = user if user and user.is_authenticated else None,
                requested_url = request.get_full_path(),
                requested_data = json.loads(request.body.decode()) if request.body else None,
                response_data = json.loads(getattr(response, 'content', b'{}').decode()) if getattr(response, 'content', None) else None
            )
        except Exception:
            pass
        return response
