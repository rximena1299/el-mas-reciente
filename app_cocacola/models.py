from django.db import models
from datetime import date
from django.utils import timezone

# ==========================================
# MODELO: CLIENTE
# ==========================================
class Cliente(models.Model):
    # Datos personales
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    genero = models.CharField(max_length=20, blank=True, null=True)  # opcional
    # Contacto / dirección
    direccion = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=100, blank=True, null=True)
    codigo_postal = models.CharField(max_length=10, blank=True, null=True)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    # Preferencias y sistema
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    preferencia = models.CharField(max_length=100, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


# ==========================================
# MODELO: PRODUCTO
# ==========================================
class Producto(models.Model):
    nombre_producto = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    stock_actual = models.IntegerField()
    fecha_fabricacion = models.DateField(default=date.today)
    fecha_vencimiento = models.DateField(default=date.today)

    def __str__(self):
        return self.nombre_producto


# ==========================================
# MODELO: PEDIDO
# (añadido, consistente con lo que pediste)
# ==========================================
class Pedido(models.Model):
    METODO_PAGO_CHOICES = [
        ('efectivo', 'Efectivo'),
        ('tarjeta', 'Tarjeta'),
        ('transferencia', 'Transferencia'),
    ]

    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pedidos')
    productos = models.ManyToManyField(Producto, through='PedidoProducto', related_name='pedidos')
    numero_pedido = models.CharField(max_length=20, unique=True)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    fecha_entrega = models.DateField(null=True, blank=True)
    direccion_envio = models.CharField(max_length=255)
    ciudad_envio = models.CharField(max_length=100, blank=True, null=True)
    codigo_postal_envio = models.CharField(max_length=10, blank=True, null=True)
    metodo_pago = models.CharField(max_length=50, choices=METODO_PAGO_CHOICES)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='pendiente')
    observaciones = models.TextField(blank=True, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    impuestos = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    envio = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Pedido #{self.numero_pedido} - {self.cliente.nombre} {self.cliente.apellido}"

    def calcular_totales(self):
        items = self.pedidoproducto_set.all()
        subtotal = sum([it.subtotal or 0 for it in items])
        impuestos = round(subtotal * 0.16, 2)  # ejemplo 16%
        envio = float(self.envio or 0)
        total = subtotal + impuestos + envio
        self.subtotal = subtotal
        self.impuestos = impuestos
        self.total = total
        self.save()


# ==========================================
# MODELO INTERMEDIO: PedidoProducto
# ==========================================
class PedidoProducto(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)  # precio al momento del pedido
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.precio_unitario is not None and self.cantidad is not None:
            self.subtotal = self.precio_unitario * self.cantidad
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre_producto} (Pedido {self.pedido.numero_pedido})"
