from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "usuarios"
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    ]