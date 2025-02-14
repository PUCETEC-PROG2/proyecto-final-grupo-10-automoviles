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
def añadir_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    compra_id = request.session.get('compra_id')
    
    if not compra_id:
        # Crear una nueva compra si no existe
        compra = Compra.objects.create(cliente=None)  # Ajustar cliente si es necesario
        request.session['compra_id'] = compra.id
    else:
        # Obtener la compra existente
        compra = Compra.objects.get(id=compra_id, estado='pendiente')

    # Verificar si el producto ya está en el carrito
    detalle, creado = DetalleCompra.objects.get_or_create(
        compra=compra,
        producto=producto,
        defaults={'cantidad': 1, 'precio_unitario': producto.precio}
    )
    if not creado:
        # Si ya existe, incrementar la cantidad
        detalle.cantidad += 1
        detalle.save()

    return redirect('compras')  # Redirige a la vista del carrito


def catalogo_carros(request):
    # Obtén o crea la categoría "Carros" si no existe
    categoria_carros, created = Categoria.objects.get_or_create(nombre="Carros")
    # Filtra los productos por categoría
    carros = Producto.objects.filter(categoria=categoria_carros)
    return render(request, 'catalogo_carros.html', {'carros': carros})

def catalogo_repuestos(request):
    categoria_repuestos, created = Categoria.objects.get_or_create(nombre="Repuestos")
    repuestos = Producto.objects.filter(categoria=categoria_repuestos)
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


@login_required
def añadir_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    compra_id = request.session.get('compra_id')
    compra = Compra.objects.filter(id=compra_id, estado='pendiente').first()

    if not compra:
        cliente = Cliente.objects.first()  # Ajustar lógica para cliente real
        if not cliente:
            messages.error(request, "No hay clientes disponibles para asignar la compra.")
            return redirect('index')
        compra = Compra.objects.create(cliente=cliente)
        request.session['compra_id'] = compra.id

    detalle, created = DetalleCompra.objects.get_or_create(
        compra=compra, producto=producto,
        defaults={'cantidad': 1, 'precio_unitario': producto.precio}
    )
    if not created:
        detalle.cantidad += 1
        detalle.save()

    messages.success(request, f"Producto '{producto.nombre}' añadido a la compra.")
    return redirect('ver_compras')

def ver_compras(request):
    compra_id = request.session.get('compra_id')
    compra = Compra.objects.filter(id=compra_id, estado='pendiente').first()

    # Calcular el total de la compra
    total = 0
    if compra:
        total = sum(detalle.cantidad * detalle.precio_unitario for detalle in compra.detallecompra_set.all())

    return render(request, 'compras.html', {'compra': compra, 'total': total})


@login_required
def finalizar_compra(request):
    compra_id = request.session.get('compra_id')
    compra = Compra.objects.filter(id=compra_id, estado='pendiente').first()
    
    if compra:
        compra.estado = 'finalizada'
        compra.total = sum(item.cantidad * item.precio_unitario for item in compra.detallecompra_set.all())
        compra.save()
        del request.session['compra_id']  # Eliminar compra de sesión

    return redirect('ver_compras')


def agregar_producto_form(request):
    return render(request, 'agregar_producto.html')

def nuevo_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')  # O la página que prefieras
    else:
        form = ProductoForm()
    return render(request, 'nuevo_producto.html', {'form': form})

def ver_compras(request):
    compra_id = request.session.get('compra_id')
    compra = Compra.objects.filter(id=compra_id, estado='pendiente').first()

    return render(request, 'compras.html', {'compra': compra})

@login_required
def eliminar_producto_carrito(request, detalle_id):
    detalle = get_object_or_404(DetalleCompra, id=detalle_id)
    compra = detalle.compra

    if compra.estado == 'pendiente':
        detalle.delete()

        # Si la compra ya no tiene detalles, eliminarla
        if not compra.detallecompra_set.exists():
            compra.delete()
            del request.session['compra_id']

    return redirect('ver_compras')
