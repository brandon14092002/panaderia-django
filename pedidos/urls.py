from django.urls import path
from . import views

urlpatterns = [
    path('imprimir/<int:pedido_id>/', views.imprimir_pedido, name='imprimir_pedido'),
]

