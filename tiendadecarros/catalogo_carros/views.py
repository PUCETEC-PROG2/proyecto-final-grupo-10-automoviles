from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Producto, Categoria, Cliente, Compra, DetalleCompra
from .forms import ProductoForm, ClienteForm, CompraForm, DetalleCompraForm
from django.utils import timezone 


def index(request):
    productos_destacados = Producto.objects.filter(destacado=True)
    return render(request, 'index.html', {'productos_destacados': productos_destacados})

@login_required
def categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    productos = categoria.productos.all()  
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


    detalles_con_subtotal = []
    for detalle in detalles:
        subtotal = detalle.cantidad * detalle.precio_unitario
        detalles_con_subtotal.append({
            'detalle': detalle,
            'subtotal': subtotal
        })

    return render(request, 'detalle_compra.html', {
        'compra': compra,
        'detalles_con_subtotal': detalles_con_subtotal
    })

@login_required
def añadir_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    compra_id = request.session.get('compra_id')
    compra = Compra.objects.filter(id=compra_id, estado='pendiente').first()

    if not compra:
        
        cliente = Cliente.objects.first()  
        if not cliente:
            messages.error(request, "No hay clientes disponibles para asignar la compra.")
            return redirect('index')

        
        compra = Compra.objects.create(
            cliente=cliente,
            fecha=timezone.now().date()  
        )
        request.session['compra_id'] = compra.id 

    
    detalle, creado = DetalleCompra.objects.get_or_create(
        compra=compra,
        producto=producto,
        defaults={'cantidad': 1, 'precio_unitario': producto.precio}
    )
    if not creado:
        
        detalle.cantidad += 1
        detalle.save()

    messages.success(request, f"Producto '{producto.nombre}' añadido al carrito.")
    return redirect('ver_compras')  
@login_required
def catalogo_carros(request):
    
    categoria_carros, created = Categoria.objects.get_or_create(nombre="Carros")
    
    carros = Producto.objects.filter(categoria=categoria_carros)
    return render(request, 'catalogo_carros.html', {'carros': carros})
@login_required
def catalogo_repuestos(request):
    categoria_repuestos, created = Categoria.objects.get_or_create(nombre="Repuestos")
    repuestos = Producto.objects.filter(categoria=categoria_repuestos)
    return render(request, 'catalogo_repuestos.html', {'repuestos': repuestos})
@login_required
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
@login_required
def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('clientes')  
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'editar_cliente.html', {'form': form, 'cliente': cliente})
@login_required
def eliminar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == "POST":  
        cliente.delete()
        return redirect('clientes')  

    return render(request, 'eliminar_cliente.html', {'cliente': cliente})



@login_required
def finalizar_compra(request):
    compra_id = request.session.get('compra_id')
    compra = Compra.objects.filter(id=compra_id, estado='pendiente').first()
    
    if compra:
        compra.estado = 'finalizada'
        compra.fecha_finalizacion = timezone.now()
        compra.total = sum(item.cantidad * item.precio_unitario for item in compra.detalles.all())  # Usa el related_name definido
        compra.save()
        del request.session['compra_id']  

    return redirect('ver_compras')
@login_required
def agregar_producto_form(request):
    return render(request, 'agregar_producto.html')
@login_required
def nuevo_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')  
    else:
        form = ProductoForm()
    return render(request, 'nuevo_producto.html', {'form': form})
@login_required
def ver_compras(request):
    compra_id = request.session.get('compra_id')
    compra = Compra.objects.filter(id=compra_id, estado='pendiente').first()

    
    total = 0
    detalles_con_subtotal = []
    if compra:
        detalles = compra.detalles.all()  
        for detalle in detalles:
            subtotal = detalle.cantidad * detalle.precio_unitario
            detalles_con_subtotal.append({
                'detalle': detalle,
                'subtotal': subtotal
            })
            total += subtotal
    else:
        detalles = []

    return render(request, 'compras.html', {
        'compra': compra,
        'detalles_con_subtotal': detalles_con_subtotal,
        'total': total
    })
    
@login_required
def eliminar_producto_carrito(request, detalle_id):
    detalle = get_object_or_404(DetalleCompra, id=detalle_id)
    compra = detalle.compra

    if compra.estado == 'pendiente':
        detalle.delete()
        messages.success(request, "Producto eliminado del carrito.")

        if not compra.detalles.exists():  
            compra.delete()
            del request.session['compra_id']

    return redirect('ver_compras')


@login_required
def historial_compras(request):
    compras_finalizadas = Compra.objects.filter(estado='finalizada').order_by('-fecha_finalizacion')
    
    return render(request, 'historial_compras.html', {'compras_finalizadas': compras_finalizadas})

def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado correctamente.')
        return redirect('index')  

    return render(request, 'confirmar_eliminar.html', {'producto': producto})
@login_required
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()  
            messages.success(request, 'Producto actualizado correctamente.')
            return redirect('index')  
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'editar_producto.html', {'form': form, 'producto': producto})
@login_required
def eliminar_repuesto(request, repuesto_id):
    repuesto = get_object_or_404(Producto, id=repuesto_id)

    if request.method == 'POST':
        repuesto.delete()
        messages.success(request, 'Repuesto eliminado correctamente.')
        return redirect('catalogo_repuestos')  

    return render(request, 'confirmar_eliminar_repuesto.html', {'repuesto': repuesto})
@login_required
def acerca_de(request):
    return render(request, 'acerca_de.html')