Django API с JWT Аутентификацией и RBAC Авторизацией
Этот проект — реализация backend-API на Django для системы аутентификации и авторизации, соответствующая тестовому заданию.
Ключевые особенности:

Аутентификация: Регистрация/логин с хэшированием паролей через bcrypt, генерация JWT-токенов через PyJWT. Идентификация пользователя по заголовку Authorization: Bearer <token>.
Авторизация: RBAC (Role-Based Access Control) с ролями, ресурсами и правилами доступа. Проверка прав в кастомных функциях.
Без DRF: Чистый Django с классовыми views, JsonResponse и middleware.
Безопасность: Мягкое удаление (is_active), экспирация токенов (24 часа), ошибки 401/403.
Мок-данные: Вымышленные ресурсы (items) для демонстрации доступа.
Тестирование: Postman/cURL (примеры ниже).

Проект использует SQLite для простоты (миграции готовы). Нет сессий/куков — чистый stateless JWT для API.

Оставил в settings SECRET_KEY, JWT_SECRET, JWT_ALGORITHM в продакшене такое убиратеся в .env, который в свою очередь убирается в .gitignore

# Клонируй репозиторий
git clone https://github.com/blackkvadrat/django-jwt-rbac-api.git
cd django-jwt-rbac-api

# Виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Установка зависимостей
pip install django bcrypt pyjwt

# Миграции
python manage.py makemigrations
python manage.py migrate

# Тестовые данные (shell)


python manage.py shell

from ttask_app.models import Role, Items, Permission, User
import bcrypt

# Роли
Role.objects.create(name='admin')
Role.objects.create(name='user')

# Ресурсы
Items.objects.create(name='items')

# Права
admin_role = Role.objects.get(name='admin')
user_role = Role.objects.get(name='user')
items = Items.objects.get(name='items')

Permission.objects.create(role=admin_role, item=items, can_view=True, can_create=True)
Permission.objects.create(role=user_role, item=items, can_view=True)

# Админ
admin = User(email='admin@example.com')
admin.set_password('123')  # Хэш через bcrypt
admin.role = admin_role
admin.is_active = True
admin.save()


1. Регистрация (POST /api/register/)
json{
  "email": "test@example.com",
  "password": "123"
}
Ответ: {"message": "Registered", "id": 1}
2. Логин (POST /api/login/)
json{
  "email": "test@example.com",
  "password": "123"
}
Ответ: {"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}
3. Профиль (GET /api/profile/)
Заголовок: Authorization: Bearer <token>
Ответ: {"email": "test@example.com", "id": 1}
4. Ресурсы (GET /api/items/)
Заголовок: Authorization: Bearer <token> (доступ по роли)
Мок: [{"id": 1, "name": "Laptop"}]

User: Только view.
Admin: View + create (расширяемо).

5. Админ: Роли (GET /api/admin/roles/)
Заголовок: Authorization: Bearer <admin_token>
Ответ: [{"id": 1, "name": "admin"}, {"id": 2, "name": "user"}]
