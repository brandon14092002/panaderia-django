from django import forms
from .models import Pedido

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = '__all__'
        widgets = {
            'sabor': forms.Select()   # 👈 fuerza a que sabor sea siempre un dropdown
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        tipo = None
        if 'tipo' in self.data:
            tipo = self.data.get('tipo')
        elif self.instance.pk:
            tipo = self.instance.tipo

        if tipo == 'normal':
            self.fields['sabor'].choices = Pedido.SABORES_NORMAL
        elif tipo == 'relleno':
            self.fields['sabor'].choices = Pedido.SABORES_RELLENO
        else:
            self.fields['sabor'].choices = [('', '---------')] + Pedido.SABORES_NORMAL + Pedido.SABORES_RELLENO