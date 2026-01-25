from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from decimal import Decimal
from django.http import JsonResponse

from clientes.models import Cliente
from cortes.models import Corte
from .models import Factura, DetalleFactura
from users.decorators import role_required
# views.py
import qrcode
from io import BytesIO
import base64

User = get_user_model()


@login_required
@role_required(['CAJERO', 'ADMIN'])
def crear_factura(request):
    cortes = Corte.objects.all()
    barberos = User.objects.filter(rol__in=['BARBERO', 'ESTILISTA'])

    if request.method == 'POST':
        telefono = request.POST.get('telefono')
        nombre = request.POST.get('nombre')
        barbero_id = request.POST.get('barbero_id')

        cliente, _ = Cliente.objects.get_or_create(
            telefono=telefono,
            defaults={'nombre': nombre}
        )

        barbero = get_object_or_404(User, id=barbero_id)

        factura = Factura.objects.create(
            cliente=cliente,
            cajero=request.user,
            barbero=barbero,
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

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'ok': True, 'factura_id': factura.id})

        return redirect('factura_crear')

    return render(request, 'facturacion/crear.html', {
        'cortes': cortes,
        'barberos': barberos,
        'barberos': User.objects.filter(rol__in=['BARBERO','ESTILISTA'])
    })


@login_required
def historial(request):
    qs = Factura.objects.all().order_by('-fecha')
    return render(request, 'facturacion/historial.html', {'facturas': qs})


@csrf_exempt
@login_required
@role_required(['CAJERO', 'ADMIN'])
def api_create_factura(request):
    import json
    data = json.loads(request.body.decode('utf-8'))

    cliente = get_object_or_404(Cliente, id=data['cliente_id'])
    barbero = get_object_or_404(User, id=data['barbero_id'])

    factura = Factura.objects.create(
        cliente=cliente,
        cajero=request.user,
        barbero=barbero,
        total=0
    )

    total = Decimal('0.00')

    for it in data.get('items', []):
        corte = get_object_or_404(Corte, id=it['corte_id'])
        cantidad = int(it.get('cantidad', 1))
        subtotal = corte.precio * cantidad

        DetalleFactura.objects.create(
            factura=factura,
            corte=corte,
            precio=corte.precio,
            cantidad=cantidad,
            subtotal=subtotal
        )

        total += subtotal

    factura.total = total
    factura.save()

    return JsonResponse({'ok': True, 'factura_id': factura.id})

@login_required
def preview_ticket(request, factura_id):
    factura = get_object_or_404(Factura, id=factura_id)
    detalles = DetalleFactura.objects.filter(factura=factura)

    return render(request, 'facturacion/ticket.html', {
        'factura': factura,
        'detalles': detalles
    })

@login_required
def preview_ticket(request, factura_id):
    factura = get_object_or_404(Factura, id=factura_id)
    detalles = DetalleFactura.objects.filter(factura=factura)

    # Generar QR con el codigo_factura (o con más info si quieres)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=6,          # tamaño más pequeño para ticket térmico
        border=2,
    )
    qr.add_data(factura.codigo_factura)   # ← aquí va el dato que quieras codificar
    # Opcional: más info
    # qr.add_data(f"https://tudominio.com/factura/{factura.codigo_factura}")
    # qr.add_data(f"Factura: {factura.codigo_factura} | Total: {factura.total}")

    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return render(request, 'facturacion/ticket.html', {
        'factura': factura,
        'detalles': detalles,
        'qr_base64': qr_base64,
    })
