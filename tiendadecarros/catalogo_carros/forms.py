from django import forms
from .models import Producto, Cliente, Compra, DetalleCompra

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'imagen', 'destacado', ]

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'direccion', 'telefono']

class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['cliente', 'fecha']

class DetalleCompraForm(forms.ModelForm):
    class Meta:
        model = DetalleCompra
        fields = ['producto', 'cantidad', 'precio_unitario']