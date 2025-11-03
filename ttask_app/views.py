from django.http import JsonResponse
import json
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import User, Role
from .permissions import check_permission, require_admin


@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email exists'}, status=400)

        user = User(email=email)
        user.set_password(password)
        user.role = Role.objects.get(name='user')
        user.save()
        return JsonResponse({'message': 'Registered', 'id': user.id})


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        try:
            user = User.objects.get(email=email, is_active=True)
            if user.check_password(password):
                token = user.generate_token()
                return JsonResponse({'token': token})
            else:
                return JsonResponse({'error': 'Wrong password'}, status=401)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status = 401)

@method_decorator(csrf_exempt, name='dispatch')
class ProfileView(View):
    def get(self, request):
        if not request.user:
            return JsonResponse({'error': 'Нет токена или неверный. Добавь заголовок Authorization: Bearer <токен>'}, status=401)
        return JsonResponse({'email': request.user.email})

@method_decorator(csrf_exempt, name='dispatch')
class ItemsView(View):
    def get(self, request):
        ok, error, code = check_permission(request.user, 'items', 'view')
        if not ok:
            return JsonResponse(error, status=code)
        return JsonResponse([{'id':1, 'name': 'Laptop'}], safe=False)

@method_decorator(csrf_exempt, name='dispatch')
class AdminRolesView(View):
    def get(self, request):
        ok, error, code = require_admin(request.user)
        if not ok:
            return JsonResponse(error, status=code)
        roles = list(Role.objects.values('id', 'name'))
        return JsonResponse(roles, safe=False)
