from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from .forms import UserCreateForm, UserUpdateForm
from .decorators import role_required

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