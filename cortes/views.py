from django.shortcuts import render
from .models import Corte
from django.contrib.auth.decorators import login_required


@login_required
def list_cortes(request):
    cortes = Corte.objects.all()
    return render(request, 'cortes/list.html', {'cortes': cortes})
