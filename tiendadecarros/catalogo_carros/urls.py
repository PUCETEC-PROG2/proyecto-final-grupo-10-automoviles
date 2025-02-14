from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('categoria/<int:categoria_id>/', views.categoria, name='categoria'),
    path('clientes/', views.clientes, name='clientes'),
    path('compras/', views.compras, name='compras'),
    path('detalle_compra/<int:compra_id>/', views.detalle_compra, name='detalle_compra'),
    path('agregar_producto/', views.añadir_producto, name='agregar_producto'),
    path('catalogo_carros/', views.catalogo_carros, name='catalogo_carros'),
    path('catalogo-repuestos/', views.catalogo_repuestos, name='catalogo_repuestos'),
    path('nuevo-cliente/', views.nuevo_cliente, name='nuevo_cliente'),
    path('editar-cliente/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    path('eliminar-cliente/<int:cliente_id>/', views.eliminar_cliente, name='eliminar_cliente'),
]