from django.urls import path
from . import views

app_name = "pedidos"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path('adicionar_marmita/', views.adicionar_marmita, name='adicionar-marmita'),
    path('remover_marmita/<int:item_id>/', views.remover_marmita, name='remover-marmita'),
    path('visualizar_carrinho/', views.visualizar_carrinho, name='visualizar-carrinho'),
    path('fechar_pedido/', views.fechar_pedido, name='fechar-pedido'),
    path('cancelar_pedido/<int:pedido_id>/', views.cancelar_pedido, name='cancelar-pedido'),
]