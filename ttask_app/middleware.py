import jwt
from django.conf import settings
from .models import User

class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', '')
        if token.startswith('Bearer '):
            token = token[7:]

        if token:
            try:
                data = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
                user = User.objects.get(id=data['user_id'], is_active=True)
                request.user = user
                return self.get_response(request)
            except:
                pass

        request.user = None
        return self.get_response(request)