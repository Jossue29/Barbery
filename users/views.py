from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .forms import UserCreateForm, UserUpdateForm, PerfilForm
from .decorators import role_required
from django.core.paginator import Paginator
from django.http import JsonResponse


User = get_user_model()

@login_required
@role_required(['ADMIN'])
def users_view(request):
    users_qs = User.objects.all().order_by('username')
    paginator = Paginator(users_qs, 10)
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)

    create_form = UserCreateForm(request.POST or None, prefix='create')

    if request.method == 'POST':
        if 'create-submit' in request.POST:
            if create_form.is_valid():
                create_form.save()
                return redirect('users')

        # Manejo de edición (buscar cuál formulario se envió)
        for user in users:
            prefix = f'edit-{user.id}'
            if f'edit-submit-{user.id}' in request.POST:
                edit_form = UserUpdateForm(request.POST, instance=user, prefix=prefix)
                if edit_form.is_valid():
                    edit_form.save()
                    return redirect('users')

    # Para GET (y para mostrar forms limpios en modales)
    for user in users:
        user.edit_form = UserUpdateForm(instance=user, prefix=f'edit-{user.id}')

    context = {
        'users': users,
        'create_form': create_form,
    }

    return render(request, 'users/list.html', context)

@login_required
def cambiar_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Contraseña actualizada correctamente')
            return redirect('perfil')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'users/cambiar_password.html', {
        'form': form
    })

@login_required
def perfil(request):
    user = request.user
    password_form = PasswordChangeForm(user)

    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Diferenciar entre cambio de perfil y cambio de contraseña
        if 'old_password' in request.POST:
            # Cambio de contraseña
            form = password_form
            form = PasswordChangeForm(user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                return JsonResponse({'ok': True})
            else:
                return JsonResponse({'ok': False, 'errors': form.errors})
        else:
            # Cambio de perfil
            form = PerfilForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                return JsonResponse({'ok': True})
            else:
                return JsonResponse({'ok': False, 'errors': form.errors})
    
    form = PerfilForm(instance=user)
    return render(request, 'users/perfil.html', {'form': form, 'password_form': password_form})