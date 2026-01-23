from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from .forms import UserCreateForm, UserUpdateForm
from .decorators import role_required

User = get_user_model()


@login_required
@role_required(['ADMIN'])
def users_view(request, pk=None):
    # ===== LISTADO CON PAGINADO =====
    qs = User.objects.all().order_by('username')
    paginator = Paginator(qs, 10)  # 10 usuarios por página
    page_number = request.GET.get('page')
    users_page = paginator.get_page(page_number)

    # ===== FORM CREATE / UPDATE =====
    if pk:
        instance = get_object_or_404(User, pk=pk)
        form = UserUpdateForm(request.POST or None, instance=instance)
        title = 'Editar usuario'
    else:
        form = UserCreateForm(request.POST or None)
        title = 'Crear usuario'

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('users')

    return render(request, 'users/list.html', {
        'users': users_page,
        'form': form,
        'title': title,
    })
