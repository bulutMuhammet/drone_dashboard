from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import RegisterView, LoginView, TeamListView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register-api'),
    path('login/', LoginView.as_view(), name='login-api'),  # Login işlemi için
    path('teams/', TeamListView.as_view(), name="teams-api")
]
