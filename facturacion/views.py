from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from decimal import Decimal
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from clientes.models import Cliente
from cortes.models import Corte
from .models import Factura, DetalleFactura
from .models import Factura, DetalleFactura, Cobro
from users.decorators import role_required
from django.db.models import Sum
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models.functions import TruncDate

# views.py
import qrcode
from io import BytesIO
import base64
from django.db.models import Sum
from django.http import JsonResponse
from django.utils import timezone

User = get_user_model()
DIA_PAGO = 5

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

from django.views.decorators.http import require_POST

@login_required
@role_required(['BARBERO', 'ESTILISTA'])
def cobro(request):
    return render(request, 'facturacion/cobro.html')


@login_required
def ajax_cargar_factura(request):
    codigo = request.GET.get('codigo')

    if not codigo:
        return JsonResponse({'ok': False, 'msg': 'Código requerido'})

    try:
        factura = Factura.objects.get(codigo_factura=codigo)
    except Factura.DoesNotExist:
        return JsonResponse({'ok': False, 'msg': 'Factura no existe'})

    # Validar que sea el mismo barbero
    if factura.barbero != request.user:
        return JsonResponse({'ok': False, 'msg': 'No puedes cobrar esta factura'})

    # Validar que no esté cobrada
    if hasattr(factura, 'cobro'):
        return JsonResponse({'ok': False, 'msg': 'Esta factura ya fue cobrada'})

    detalles = []
    for d in factura.detalles.all():
        detalles.append({
            'corte': d.corte.nombre_corte,
            'precio': float(d.precio),
            'cantidad': d.cantidad,
            'subtotal': float(d.subtotal),
        })

    return JsonResponse({
        'ok': True,
        'factura': {
            'codigo': factura.codigo_factura,
            'cliente': factura.cliente.nombre,
            'fecha': factura.fecha.strftime('%d/%m/%Y %H:%M'),
            'total': float(factura.total),
            'comision': float(factura.total * Decimal('0.5')),
            'detalles': detalles
        }
    })

@login_required
@require_POST
@role_required(['BARBERO', 'ESTILISTA'])
def ajax_cobrar_factura(request):
    codigo = request.POST.get('codigo')
    try:
        factura = Factura.objects.get(codigo_factura=codigo)
    except Factura.DoesNotExist:
        return JsonResponse({'ok': False, 'msg': 'Factura no existe'})

    # Validar barbero
    if factura.barbero != request.user:
        return JsonResponse({'ok': False, 'msg': 'No puedes cobrar esta factura'})

    # Validar cobro duplicado
    if hasattr(factura, 'cobro'):
        return JsonResponse({'ok': False, 'msg': 'Factura ya cobrada'})

    comision = factura.total * Decimal('0.5')
    Cobro.objects.create(barbero=request.user, factura=factura, monto=comision)

    return JsonResponse({'ok': True, 'msg': f'Cobro realizado: C$ {comision:.2f}'})

@login_required
@role_required(['BARBERO', 'ESTILISTA'])
def mis_cobros(request):
    # Solo cobros no pagados
    cobros = Cobro.objects.filter(barbero=request.user, pagado=False).select_related('factura','factura__cliente')
    total_cobros = sum(c.monto for c in cobros)
    return render(request, 'facturacion/cobro.html', {'cobros': cobros, 'total_cobros': total_cobros})

@login_required
@role_required(['BARBERO', 'ESTILISTA'])
def ajax_mis_cobros(request):
    cobros = Cobro.objects.filter(barbero=request.user, pagado=False).select_related('factura', 'factura__cliente')
    data = []
    total = 0
    for c in cobros:
        data.append({
            'id': c.id,
            'codigo': c.factura.codigo_factura,
            'cliente': c.factura.cliente.nombre,
            'fecha': c.factura.fecha.strftime("%d/%m/%Y"),
            'monto': float(c.monto)
        })
        total += float(c.monto)

    return JsonResponse({'ok': True, 'cobros': data, 'total': total})

@login_required
@role_required(['ADMIN', 'CAJERO'])
def historial_facturas(request):
    filtro = request.GET.get('filtro', 'hoy')
    barbero_id = request.GET.get('barbero')
    hoy = timezone.localdate()

    # Queryset base
    facturas = Factura.objects.select_related('barbero', 'cliente').order_by('-fecha')

    # 🔥 Filtro por fecha usando TruncDate para zona horaria
    if filtro == 'hoy':
        facturas = facturas.annotate(
            fecha_local=TruncDate('fecha', tzinfo=timezone.get_current_timezone())
        ).filter(fecha_local=hoy)
    elif filtro == 'semana':
        inicio_semana = hoy - timedelta(days=hoy.weekday())
        fin_semana = inicio_semana + timedelta(days=6)
        facturas = facturas.annotate(
            fecha_local=TruncDate('fecha', tzinfo=timezone.get_current_timezone())
        ).filter(fecha_local__range=(inicio_semana, fin_semana))

    # 🔹 Filtro por barbero (agregado)
    if barbero_id:
        facturas = facturas.filter(barbero_id=barbero_id)

    print('FACTURAS:', facturas.count())
    print('BARBERO:', barbero_id)

    # Crear lista de facturas
    facturas_list = []
    total_facturado = Decimal('0.00')
    total_comision_negocio = Decimal('0.00')

    for f in facturas:
        comision = f.total * Decimal('0.5')
        facturas_list.append({
            'codigo': f.codigo_factura,
            'cliente': f.cliente.nombre,
            'barbero': f.barbero.get_full_name() or f.barbero.username,
            'fecha': f.fecha,
            'total': f.total,
            'comision_negocio': comision
        })
        total_facturado += f.total
        total_comision_negocio += comision

    # Total pendiente por barbero
    total_pendiente = Decimal('0.00')
    if barbero_id:
        total_pendiente = Cobro.objects.filter(
            barbero_id=barbero_id,
            pagado=False
        ).aggregate(total=Sum('monto'))['total'] or Decimal('0.00')

    # Lista de barberos para el select
    barberos = User.objects.filter(rol__in=['BARBERO', 'ESTILISTA'])

    return render(request, 'facturacion/historial.html', {
        'facturas': facturas_list,
        'total_facturado': total_facturado,
        'total_comision_negocio': total_comision_negocio,
        'total_pendiente': total_pendiente,
        'barberos': barberos,
        'barbero_id': barbero_id,
        'filtro': filtro,
        'es_dia_pago': timezone.now().weekday() == DIA_PAGO
    })

@login_required
@role_required(['ADMIN', 'CAJERO'])
def pagar_cobros_barbero(request):
    barbero_id = request.POST.get('barbero_id')

    if not barbero_id:
        return JsonResponse({'ok': False, 'msg': 'Barbero no válido'})

    # Solo cobros pendientes
    cobros = Cobro.objects.filter(
        barbero_id=barbero_id,
        pagado=False
    )

    if not cobros.exists():
        return JsonResponse({'ok': False, 'msg': 'Este barbero ya no tiene cobros pendientes'})

    # Marcar como pagados
    cantidad = cobros.update(
        pagado=True,
        fecha=timezone.now()
    )

    return JsonResponse({
        'ok': True,
        'msg': f'Pago realizado correctamente ({cantidad} cobros marcados como pagados)'
    })