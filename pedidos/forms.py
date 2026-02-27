from django import forms
from .models import Pedido

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = '__all__'
        widgets = {
            'fecha_pedido': forms.DateInput(attrs={'type': 'date'}),
            'fecha_entrega': forms.DateInput(attrs={'type': 'date'}),
            'hora_pedido': forms.TimeInput(attrs={'type': 'time'}),
            'hora_entrega': forms.TimeInput(attrs={'type': 'time'}),
            'sabor': forms.Select()   # 👈 fuerza a que sabor sea siempre un dropdown
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        tipo = None
        # Si el formulario viene con datos (ej. POST)
        if 'tipo' in self.data:
            tipo = self.data.get('tipo')
        # Si estamos editando un pedido existente
        elif self.instance.pk:
            tipo = self.instance.tipo

        # Filtrar sabores según el tipo
        if tipo == 'normal':
            self.fields['sabor'].choices = Pedido.SABORES_NORMAL
        elif tipo == 'relleno':
            self.fields['sabor'].choices = Pedido.SABORES_RELLENO
        else:
            # Si no hay tipo seleccionado aún, mostrar todas las opciones
            self.fields['sabor'].choices = [('', '---------')] + Pedido.SABORES_NORMAL + Pedido.SABORES_RELLENO