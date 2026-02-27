from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Pedido, Precio, PrecioFormaTipoSabor
from .forms import PedidoForm

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    form = PedidoForm   # formulario dinámico para sabores según tipo

    list_display = (
        'id',
        'nombre',
        'tipo',
        'forma',
        'sabor',
        'diseno_torta',
        'dibujo_mano',
        'perlas',
        'papel_dorado',
        'papel_plateado',
        'flores_comestibles',
        'flores_reales',
        'impresion_foto',
        'impresion_arroz',
        'base_entrega',
        'estado',
        'total',
        'observacion',
        'imprimir_link',   # 👈 botón de impresión
    )
    list_filter = ('tipo', 'forma', 'estado', 'diseno_torta', 'dibujo_mano')
    search_fields = ('nombre', 'celular', 'responsable')
    readonly_fields = ('total',)

    fieldsets = (
        ('Datos del cliente', {
            'fields': ('nombre', 'celular', 'responsable')
        }),
        ('Fechas y horas', {
            'fields': ('fecha_pedido', 'fecha_entrega', 'hora_pedido', 'hora_entrega')
        }),
        ('Tipo de pastel', {
            'fields': ('tipo', 'sabor')
        }),
        ('Forma y tamaño', {
            'fields': ('forma',)
        }),
        ('Diseño', {
            'fields': (
                'diseno_torta',
                'dibujo_mano',
                'perlas',
                'papel_dorado',
                'papel_plateado',
                'flores_comestibles',
                'flores_reales'
            )
        }),
        ('Impresión', {
            'fields': ('impresion_foto','impresion_arroz')
        }),
        ('Base de entrega', {
            'fields': ('base_entrega',)
        }),
        ('Contrato', {
            'fields': ('imagen','observacion','total','abono','estado')
        }),
    )

    class Media:
        # 👇 aquí puedes agregar JS/CSS personalizados si quieres mejorar la UI
        js = ('js/pedido_admin.js',)
        css = {
            'all': ('css/pedido_admin.css',)  # opcional: estilos personalizados
        }

    # 👇 Método para mostrar el botón de impresión
    def imprimir_link(self, obj):
        url = reverse('imprimir_pedido', args=[obj.id])
        return format_html('<a href="{}" target="_blank">🖨️ Imprimir</a>', url)
    imprimir_link.short_description = "Imprimir"


@admin.register(Precio)
class PrecioAdmin(admin.ModelAdmin):
    list_display = ('categoria', 'opcion', 'valor')
    list_filter = ('categoria',)
    search_fields = ('opcion',)


@admin.register(PrecioFormaTipoSabor)
class PrecioFormaTipoSaborAdmin(admin.ModelAdmin):
    list_display = ('forma', 'tipo', 'sabor', 'valor')
    list_filter = ('forma', 'tipo', 'sabor')
    search_fields = ('forma', 'tipo', 'sabor')