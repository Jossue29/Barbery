from django.shortcuts import render, redirect
from .models import Corte
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

@login_required
def list_cortes(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre_corte')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')

        Corte.objects.create(
            nombre_corte=nombre,
            descripcion=descripcion,
            precio=precio
        )
        return redirect('cortes_list')

    cortes = Corte.objects.all()
    print(cortes)  # Esto muestra el QuerySet en la consola
    for c in cortes:
        print(c.id, c.nombre_corte, c.precio, c.descripcion)
    return render(request, 'cortes/list.html', {'cortes': cortes})

def editar_corte(request, corte_id):
    corte = get_object_or_404(Corte, id=corte_id)
    if request.method == "POST":
        corte.nombre = request.POST.get("nombre")
        corte.descripcion = request.POST.get('descripcion')
        corte.precio = request.POST.get("precio")
        corte.save()
        return redirect('cortes_list')