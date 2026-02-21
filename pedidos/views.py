from django.shortcuts import render, get_object_or_404
from .models import Pedido

def imprimir_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, 'pedidos/imprimir_pedido.html', {'pedido': pedido})