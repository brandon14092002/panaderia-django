from django.db import models
from decimal import Decimal

class Precio(models.Model):
    categoria = models.CharField(max_length=50)   # sabor, agregado, base
    opcion = models.CharField(max_length=50)      # chocolate, impresion_foto, plana, etc.
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.categoria} - {self.opcion}: {self.valor}"


class PrecioFormaTipoSabor(models.Model):
    forma = models.CharField(max_length=50)   # circular_0, cuadrada_1, plancha_1, etc.
    tipo = models.CharField(max_length=50)    # normal, relleno
    sabor = models.CharField(max_length=50)   # naranja, tres_leches, etc.
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.forma} + {self.tipo} + {self.sabor}: {self.valor}"


class Pedido(models.Model):
    # -------------------------
    # Datos del cliente
    # -------------------------
    nombre = models.CharField(max_length=100)
    celular = models.CharField(max_length=10)
    responsable = models.CharField(max_length=100)
    fecha = models.DateField()
    hora = models.TimeField()

    # -------------------------
    # Tipo de pastel
    # -------------------------
    TIPOS = [
        ('normal', 'Normal'),
        ('relleno', 'Relleno'),
    ]
    tipo = models.CharField(max_length=30, choices=TIPOS)

    # -------------------------
    # Sabores según tipo
    # -------------------------
    SABORES_NORMAL = [
        ('vainilla', 'Vainilla'),
        ('frutilla', 'Frutilla'),
        ('chocolate', 'Chocolate'),
    ]
    SABORES_RELLENO = [
        ('naranja', 'Naranja'),
        ('tres_leches', 'Tres Leches'),
        ('chocolate', 'Chocolate'),
    ]
    sabor = models.CharField(max_length=30, blank=True, null=True)

    FORMAS = [
        ('circular_0', 'N#0 Circular (4 pers.)'),
        ('circular_1', 'N#1 Circular (8 pers.)'),
        ('circular_2', 'N#2 Circular (12 pers.)'),
        ('circular_3', 'N#3 Circular (18 pers.)'),
        ('circular_4', 'N#4 Circular (25 pers.)'),
        ('cuadrada_1', 'N#1 Cuadrada (12 pers.)'),
        ('cuadrada_2', 'N#2 Cuadrada (18 pers.)'),
        ('cuadrada_3', 'N#3 Cuadrada (25 pers.)'),
        ('plancha_1_2', 'Media Plancha (30 pers.)'),
        ('plancha_1', 'Plancha (60 pers.)'),
    ]
    forma = models.CharField(max_length=20, choices=FORMAS)

    # -------------------------
    # Diseño y agregados
    # -------------------------
    DISENOS_TORTA = [
        ('facil', 'Diseño Fácil'),
        ('medio', 'Diseño Medio'),
        ('dificil', 'Diseño Difícil'),
    ]
    diseno_torta = models.CharField(
        "Diseño de torta",
        max_length=20,
        choices=DISENOS_TORTA,
        default='facil'
    )

    DIBUJOS = [
        ('facil', 'Fácil'),
        ('medio', 'Medio'),
        ('dificil', 'Difícil'),
    ]
    dibujo_mano = models.CharField(max_length=20, choices=DIBUJOS, blank=True, null=True)

    perlas = models.PositiveIntegerField(default=0)
    papel_dorado = models.PositiveIntegerField(default=0)
    papel_plateado = models.PositiveIntegerField(default=0)
    flores_comestibles = models.PositiveIntegerField(default=0)
    flores_reales = models.PositiveIntegerField(default=0)
    impresion_foto = models.PositiveIntegerField(default=0)

    # 👇 ahora DecimalField para permitir fracciones (ejemplo: 0.5 papel arroz)
    impresion_arroz = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    BASES = [
        ('plana', 'Plana'),
        ('alta', 'Alta'),
        ('sencilla', 'Sencilla'),
    ]
    base_entrega = models.CharField(max_length=20, choices=BASES, blank=True, null=True)

    # -------------------------
    # Imagen del pedido
    # -------------------------
    imagen = models.ImageField(upload_to='pedidos_fotos/', blank=True, null=True)

    # -------------------------
    # Observaciones
    # -------------------------
    observacion = models.TextField(blank=True, null=True)

    # -------------------------
    # Contrato
    # -------------------------
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    abono = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('entregado', 'Entregado'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')

    # -------------------------
    # Métodos
    # -------------------------
    def calcular_precio(self):
        total = Decimal("0.00")

        # Precio base según forma + tipo + sabor
        try:
            total += PrecioFormaTipoSabor.objects.get(
                forma=self.forma,
                tipo=self.tipo,
                sabor=self.sabor
            ).valor
        except PrecioFormaTipoSabor.DoesNotExist:
            pass

        # Diseño de torta
        if self.diseno_torta == 'facil':
            total += Decimal("0.00")
        elif self.diseno_torta == 'medio':
            total += Decimal("1.00")
        elif self.diseno_torta == 'dificil':
            total += Decimal("2.00")

        # Dibujo a mano
        if self.dibujo_mano == 'facil':
            total += Decimal("1.00")
        elif self.dibujo_mano == 'medio':
            total += Decimal("2.00")
        elif self.dibujo_mano == 'dificil':
            total += Decimal("3.00")

        # --- Reglas especiales para perlas ---
        if self.perlas in [1, 2]:
            total += Decimal("1.00")
        elif self.perlas == 3:
            total += Decimal("2.00")
        elif self.perlas in [4, 5]:
            total += Decimal("3.00")

        # --- Reglas especiales para papel dorado ---
        if self.papel_dorado in [1, 2]:
            total += Decimal("1.00")
        elif self.papel_dorado == 3:
            total += Decimal("2.00")
        elif self.papel_dorado in [4, 5]:
            total += Decimal("3.00")

        # --- Reglas especiales para papel plateado ---
        if self.papel_plateado in [1, 2]:
            total += Decimal("1.00")
        elif self.papel_plateado == 3:
            total += Decimal("2.00")
        elif self.papel_plateado in [4, 5]:
            total += Decimal("3.00")

        total += self.flores_comestibles * Decimal("0.50")
        total += self.flores_reales * Decimal("0.25")
        total += self.impresion_foto * Decimal("3.00")

        # 👇 ahora permite fracciones de papel arroz
        total += self.impresion_arroz * Decimal("7.00")

        # Base de entrega
        if self.base_entrega:
            try:
                total += Precio.objects.get(categoria='base', opcion=self.base_entrega).valor
            except Precio.DoesNotExist:
                pass

        return total

    def save(self, *args, **kwargs):
        self.total = self.calcular_precio()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pedido {self.id} - {self.nombre} - Total: {self.calcular_precio()}"