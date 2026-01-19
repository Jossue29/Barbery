from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .decorators import role_required
from .forms import UserCreateForm, UserUpdateForm

User = get_user_model()


@login_required
def dashboard(request):
    role = request.user.rol if hasattr(request.user, 'rol') else None
    template = 'users/dashboard.html'
    return render(request, template, {'role': role})


@login_required
@role_required(['ADMIN'])
def users_list(request):
    qs = User.objects.all().order_by('username')
    return render(request, 'users/list.html', {'users': qs})


@login_required
@role_required(['ADMIN'])
def users_create(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users_list')
    else:
        form = UserCreateForm()
    return render(request, 'users/form.html', {'form': form, 'title': 'Crear usuario'})


@login_required
@role_required(['ADMIN'])
def users_update(request, pk):
    u = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=u)
        if form.is_valid():
            form.save()
            return redirect('users_list')
    else:
        form = UserUpdateForm(instance=u)
    return render(request, 'users/form.html', {'form': form, 'title': 'Editar usuario'})


@login_required
@role_required(['ADMIN'])
def users_delete(request, pk):
    u = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        u.delete()
        return redirect('users_list')
    return render(request, 'users/confirm_delete.html', {'object': u})
