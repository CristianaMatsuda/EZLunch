from django.urls import path
from . import views

app_name = "frete"
urlpatterns = [
    path("", views.index, name="index"), # Ex: /frete/
]