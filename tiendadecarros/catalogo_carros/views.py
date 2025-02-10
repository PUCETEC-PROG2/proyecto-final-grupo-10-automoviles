from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Producto, Categoria, Cliente, Compra, DetalleCompra
from .forms import ProductoForm, ClienteForm, CompraForm, DetalleCompraForm
# Create your views here.

def index(request):
    productos_destacados = Producto.objects.filter(destacado=True)
    return render(request, 'index.html', {'productos_destacados': productos_destacados})

@login_required
def categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    productos = Producto.objects.filter(categoria=categoria)
    return render(request, 'categoria.html', {'categoria': categoria, 'productos': productos})

@login_required
def clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes.html', {'clientes': clientes})

@login_required
def compras(request):
    compras = Compra.objects.all().order_by('-fecha')
    return render(request, 'compras.html', {'compras': compras})

@login_required
def detalle_compra(request, compra_id):
    compra = get_object_or_404(Compra, id=compra_id)
    detalles = DetalleCompra.objects.filter(compra=compra)
    return render(request, 'detalle_compra.html', {'compra': compra, 'detalles': detalles})

@login_required
def añadir_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)  # request.FILES para manejar la imagen
        if form.is_valid():
            form.save()  # Guarda el producto en la base de datos
            return redirect('index')  # Redirige a la página principal
    else:
        form = ProductoForm()  # Muestra un formulario vacío

    return render(request, 'añadir_producto.html', {'form': form})

def catalogo_carros(request):
    # Suponiendo que la categoría "Carros" tiene un ID específico
    categoria_carros = Categoria.objects.get(nombre="Carros")
    carros = Producto.objects.filter(categoria=categoria_carros)
    return render(request, 'catalogo_carros.html', {'carros': carros})

def catalogo_repuestos(request):
    # Suponiendo que la categoría "Repuestos" tiene un ID específico
    categoria_repuestos = Categoria.objects.get(nombre="Repuestos")
    repuestos = Producto.objects.filter(categoria=categoria_repuestos)
    return render(request, 'catalogo_repuestos.html', {'repuestos': repuestos})