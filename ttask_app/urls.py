from django.urls import path

from .views import RegisterView, LoginView, ProfileView, ItemsView, AdminRolesView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('items/', ItemsView.as_view()),
    path('admin/roles/', AdminRolesView.as_view()),
]
