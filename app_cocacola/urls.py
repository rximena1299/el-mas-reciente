from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio_cocacola, name='inicio_cocacola'),

    # Clientes
    path('cliente/agregar/', views.agregar_cliente, name='agregar_cliente'),
    path('cliente/ver/', views.ver_cliente, name='ver_cliente'),
    path('cliente/<int:cliente_id>/actualizar/', views.actualizar_cliente, name='actualizar_cliente'),
    path('cliente/<int:cliente_id>/realizar_actualizacion/', views.realizar_actualizacion_cliente, name='realizar_actualizacion_cliente'),
    path('cliente/<int:cliente_id>/borrar/', views.borrar_cliente, name='borrar_cliente'),

    path('agregar_producto/', views.agregar_producto, name='agregar_producto'),
    path('ver_producto/', views.ver_producto, name='ver_producto'),
    path('actualizar_producto/<int:id>/', views.actualizar_producto, name='actualizar_producto'),
    path('realizar_actualizacion_producto/<int:id>/', views.realizar_actualizacion_producto, name='realizar_actualizacion_producto'),
    path('borrar_producto/<int:id>/', views.borrar_producto, name='borrar_producto'),

    # ... rutas cliente y producto ...
    path('pedido/agregar/', views.agregar_pedido, name='agregar_pedido'),
    path('pedido/ver/', views.ver_pedido, name='ver_pedido'),
    path('pedido/actualizar/<int:pedido_id>/', views.actualizar_pedido, name='actualizar_pedido'),
    path('pedido/realizar_actualizacion/<int:pedido_id>/', views.realizar_actualizacion_pedido, name='realizar_actualizacion_pedido'),
    path('pedido/borrar/<int:pedido_id>/', views.borrar_pedido, name='borrar_pedido'),
]