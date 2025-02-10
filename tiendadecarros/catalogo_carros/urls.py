from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('categoria/<int:categoria_id>/', views.categoria, name='categoria'),
    path('clientes/', views.clientes, name='clientes'),
    path('compras/', views.compras, name='compras'),
    path('detalle_compra/<int:compra_id>/', views.detalle_compra, name='detalle_compra'),
    path('añadir-producto/', views.añadir_producto, name='añadir_producto'),
    path('catalogo-carros/', views.catalogo_carros, name='catalogo_carros'),
    path('catalogo-repuestos/', views.catalogo_repuestos, name='catalogo_repuestos'),
]