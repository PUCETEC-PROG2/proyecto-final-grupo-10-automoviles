from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Producto, Categoria, Cliente, Compra, DetalleCompra
from .forms import ProductoForm, ClienteForm, CompraForm, DetalleCompraForm

def index(request):
    productos_destacados = Producto.objects.filter(destacado=True)
    return render(request, 'index.html', {'productos_destacados': productos_destacados})

@login_required
def categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    productos = categoria.productos.all()  # Usa related_name
    return render(request, 'categoria.html', {'categoria': categoria, 'productos': productos})

@login_required
def clientes(request):
    clientes = Cliente.objects.all().order_by('nombre')
    return render(request, 'clientes.html', {'clientes': clientes})

@login_required
def compras(request):
    compras = Compra.objects.all().order_by('-fecha')
    return render(request, 'compras.html', {'compras': compras})

@login_required
def detalle_compra(request, compra_id):
    compra = get_object_or_404(Compra.objects.prefetch_related('detalles__producto'), id=compra_id)
    detalles = compra.detalles.all()
    return render(request, 'detalle_compra.html', {'compra': compra, 'detalles': detalles})

@login_required
def añadir_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Producto añadido correctamente!")
            return redirect('index')
    else:
        form = ProductoForm()
    return render(request, 'añadir_producto.html', {'form': form})

def catalogo_carros(request):
    categoria_carros = get_object_or_404(Categoria, nombre="carros")
    carros = categoria_carros.productos.all()
    return render(request, 'catalogo_carros.html', {'carros': carros})

def catalogo_repuestos(request):
    categoria_repuestos = get_object_or_404(Categoria, nombre="Repuestos")
    repuestos = categoria_repuestos.productos.all()
    return render(request, 'catalogo_repuestos.html', {'repuestos': repuestos})

def nuevo_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Cliente registrado correctamente!")
            return redirect('clientes')
    else:
        form = ClienteForm()
    return render(request, 'nuevo_cliente.html', {'form': form})

def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('clientes')  # Redirige a la lista de clientes
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'editar_cliente.html', {'form': form, 'cliente': cliente})

def eliminar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == "POST":  # Solo eliminar cuando se confirma en un formulario
        cliente.delete()
        return redirect('clientes')  # Redirige a la lista de clientes después de eliminar

    return render(request, 'eliminar_cliente.html', {'cliente': cliente})
