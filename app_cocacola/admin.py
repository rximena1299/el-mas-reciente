from django.contrib import admin
from .models import Cliente, Producto, Pedido, PedidoProducto

class PedidoProductoInline(admin.TabularInline):
    model = PedidoProducto
    extra = 1
    readonly_fields = ('subtotal',)

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id','numero_pedido','cliente','fecha_pedido','estado','total')
    search_fields = ('numero_pedido','cliente__nombre','cliente__apellido')
    inlines = [PedidoProductoInline]

admin.site.register(Cliente)
admin.site.register(Producto)
