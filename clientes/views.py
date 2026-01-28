from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Cliente
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q


@login_required
def list_clientes(request):
    q = request.GET.get('q', '').strip()
    clientes = Cliente.objects.all()

    if q:
        clientes = clientes.filter(Q(nombre__icontains=q) | Q(telefono__icontains=q))

    paginator = Paginator(clientes, 10)  # 10 clientes por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'clientes/list.html', {'clientes': page_obj, 'page_obj': page_obj})


def api_search_cliente(request):
    telefono = request.GET.get('telefono')
    if not telefono:
        return JsonResponse({'ok': False, 'error': 'no telefono'})
    try:
        c = Cliente.objects.get(telefono=telefono)
        return JsonResponse({'ok': True, 'cliente': {'id': c.id, 'nombre': c.nombre, 'telefono': c.telefono}})
    except Cliente.DoesNotExist:
        return JsonResponse({'ok': False})


@csrf_exempt
@require_POST
def crear_cliente_ajax(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    telefono = request.POST.get('telefono')
    nombre = request.POST.get('nombre')

    if not telefono or not nombre:
        return JsonResponse({'error': 'Datos incompletos'}, status=400)

    telefono = telefono.strip().replace(" ", "")

    cliente, created = Cliente.objects.get_or_create(
        telefono=telefono,
        defaults={'nombre': nombre}
    )

    return JsonResponse({
        'id': cliente.id,
        'telefono': cliente.telefono,
        'nombre': cliente.nombre,
        'created': created,  # 👈 clave
        'message': 'Cliente creado' if created else 'Cliente ya existe'
    })

def buscar_cliente_ajax(request):
    telefono = request.GET.get('telefono', '').replace(' ', '')  # usa 'telefono'
    
    # solo buscamos si tiene exactamente 8 dígitos
    if len(telefono) != 8:
        return JsonResponse({'exists': False})

    try:
        cliente = Cliente.objects.get(telefono=telefono)
        return JsonResponse({
            'exists': True,
            'id': cliente.id,
            'nombre': cliente.nombre,
            'telefono': cliente.telefono
        })
    except Cliente.DoesNotExist:
        return JsonResponse({'exists': False})