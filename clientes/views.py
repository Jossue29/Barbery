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
def api_create_cliente(request):
    nombre = request.POST.get('nombre')
    telefono = request.POST.get('telefono')
    if not nombre or not telefono:
        return JsonResponse({'ok': False, 'error': 'missing'})
    c, created = Cliente.objects.get_or_create(telefono=telefono, defaults={'nombre': nombre})
    return JsonResponse({'ok': True, 'cliente': {'id': c.id, 'nombre': c.nombre, 'telefono': c.telefono}})
