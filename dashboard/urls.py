from django.urls import path

from dashboard.views import LoginTemplateView, DashboardView, LogoutView, RegisterTemplateView, DroneListTemplateView, ProduceDroneTemplateView

urlpatterns = [
    path('', DashboardView.as_view(), name='index'),
    path('drone-list', DroneListTemplateView.as_view(), name='drone_list'),
    path('create-list', ProduceDroneTemplateView.as_view(), name='create_drone'),
    path('login', LoginTemplateView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('register', RegisterTemplateView.as_view(), name='register')
]
