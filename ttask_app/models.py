from datetime import datetime, timedelta
import bcrypt
import jwt
from django.db import models
from django.conf import settings


class User(models.Model):
    email = models.EmailField(unique=True, verbose_name="User's email")
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    password_hash = models.CharField(max_length=255)
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)

    def set_password(self, password):
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode(), salt).decode()

    def check_password(self, password):
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())

    def generate_token(self):
        payload = {
            'user_id': self.id,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }
        return jwt.encode(payload, settings.JWT_SECRET, algorithm='HS256')

    def __str__(self):
        return self.email

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name

class Items(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class Permission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    can_view = models.BooleanField(default=False)
    can_create = models.BooleanField(default=False)

    class Meta:
        unique_together = ('role', 'item')


