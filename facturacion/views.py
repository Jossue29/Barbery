from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from clientes.models import Cliente
from cortes.models import Corte
from .models import Factura, DetalleFactura
from django.contrib.auth import get_user_model
from decimal import Decimal
from users.decorators import role_required
from django.shortcuts import render, redirect

User = get_user_model()


@login_required
@role_required(['CAJERO', 'ADMIN'])
def crear_factura(request):
    # page with AJAX-driven form
    cortes = Corte.objects.all()
    barberos = User.objects.filter(rol='BARBERO')
    return render(request, 'facturacion/crear.html', {'cortes': cortes, 'barberos': barberos})


@csrf_exempt
@login_required
@role_required(['CAJERO', 'ADMIN'])
def api_create_factura(request):
    # Expects JSON: cliente_id, barbero_id, cajero_id, items: [{corte_id, cantidad}]
    import json
    data = json.loads(request.body.decode('utf-8'))
    cliente_id = data.get('cliente_id')
    barbero_id = data.get('barbero_id')
    items = data.get('items', [])
    cliente = get_object_or_404(Cliente, id=cliente_id)
    barbero = get_object_or_404(User, id=barbero_id)
    cajero = request.user
    total = Decimal('0.00')
    factura = Factura(cliente=cliente, cajero=cajero, barbero=barbero, total=total)
    factura.save()
    for it in items:
        corte = get_object_or_404(Corte, id=it.get('corte_id'))
        cantidad = int(it.get('cantidad', 1))
        precio = corte.precio
        subtotal = precio * cantidad
        DetalleFactura.objects.create(factura=factura, corte=corte, precio=precio, cantidad=cantidad, subtotal=subtotal)
        total += subtotal
    factura.total = total
    factura.save()
    return JsonResponse({'ok': True, 'factura_id': factura.id, 'codigo': factura.codigo_factura})


@login_required
def preview_ticket(request, factura_id):
    factura = get_object_or_404(Factura, id=factura_id)
    return render(request, 'facturacion/ticket.html', {'factura': factura})


@login_required
def historial(request):
    qs = Factura.objects.all().order_by('-fecha')
    return render(request, 'facturacion/historial.html', {'facturas': qs})

def crear_factura(request):
    cortes = Corte.objects.all()

    if request.method == 'POST':
        telefono = request.POST.get('telefono')
        nombre = request.POST.get('nombre')

        cliente, _ = Cliente.objects.get_or_create(
            telefono=telefono,
            defaults={'nombre': nombre}
        )

        factura = Factura.objects.create(
            cliente=cliente,
            cajero=request.user,
            barbero=request.user,
            total=0
        )

        total = Decimal('0.00')

        ids = request.POST.getlist('corte_id[]')
        precios = request.POST.getlist('precio[]')
        cantidades = request.POST.getlist('cantidad[]')
        subtotales = request.POST.getlist('subtotal[]')

        for i in range(len(ids)):
            DetalleFactura.objects.create(
                factura=factura,
                corte_id=ids[i],
                precio=precios[i],
                cantidad=cantidades[i],
                subtotal=subtotales[i]
            )
            total += Decimal(subtotales[i])

        factura.total = total
        factura.save()

        return redirect('factura_crear')

    return render(request, 'facturacion/crear.html', {
        'cortes': cortes
    })