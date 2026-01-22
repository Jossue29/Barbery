from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Cliente
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


@login_required
def list_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/list.html', {'clientes': clientes})


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
    if request.method == 'POST':
        telefono = request.POST.get('telefono')
        nombre = request.POST.get('nombre')

        cliente, _ = Cliente.objects.get_or_create(
            telefono=telefono,
            defaults={'nombre': nombre}
        )

        return JsonResponse({
            'id': cliente.id,
            'telefono': cliente.telefono,
            'nombre': cliente.nombre
        })
    
def api_create_cliente(request):
    if request.method == 'POST':
        telefono = request.POST.get('telefono')
        nombre = request.POST.get('nombre')

        if not telefono or not nombre:
            return JsonResponse({'error': 'Datos incompletos'}, status=400)

        cliente, created = Cliente.objects.get_or_create(
            telefono=telefono,
            defaults={'nombre': nombre}
        )

        return JsonResponse({
            'id': cliente.id,
            'nombre': cliente.nombre,
            'created': created
        })

    return JsonResponse({'error': 'Método no permitido'}, status=405)

def buscar_cliente_ajax(request):
    q = request.GET.get('q', '')
    clientes = Cliente.objects.filter(nombre__icontains=q)[:10]

    data = [
        {
            'id': c.id,
            'nombre': c.nombre,
            'telefono': c.telefono
        }
        for c in clientes
    ]

    return JsonResponse(data, safe=False)