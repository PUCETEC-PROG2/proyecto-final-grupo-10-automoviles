from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('categoria/<int:categoria_id>/', views.categoria, name='categoria'),
    path('clientes/', views.clientes, name='clientes'),
    path('compras/', views.compras, name='compras'),
    path('compras/agregar/<int:producto_id>/', views.añadir_producto, name='añadir_producto'),
    path('compras/finalizar/', views.finalizar_compra, name='finalizar_compra'),
    path('compras/eliminar/<int:detalle_id>/', views.eliminar_producto_carrito, name='eliminar_producto_carrito'),
    path('detalle_compra/<int:compra_id>/', views.detalle_compra, name='detalle_compra'),
    path('productos/nuevo/', views.nuevo_producto, name='nuevo_producto'),
    path('catalogo_carros/', views.catalogo_carros, name='catalogo_carros'),
    path('catalogo-repuestos/', views.catalogo_repuestos, name='catalogo_repuestos'),
    path('nuevo-cliente/', views.nuevo_cliente, name='nuevo_cliente'),
    path('editar-cliente/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    path('eliminar-cliente/<int:cliente_id>/', views.eliminar_cliente, name='eliminar_cliente'),
]