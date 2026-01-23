from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group

User = get_user_model()


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'username', 'nombre', 'apellido', 'telefono',
            'identidad', 'direccion', 'email', 'rol'
        )

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()
            self._assign_group(user)

        return user

    def _assign_group(self, user):
        # Limpia grupos anteriores
        user.groups.clear()

        # Asigna grupo según rol
        group, _ = Group.objects.get_or_create(name=user.rol)
        user.groups.add(group)


class UserUpdateForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = (
            'username', 'nombre', 'apellido', 'telefono',
            'identidad', 'direccion', 'email', 'rol'
        )

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()
            self._assign_group(user)

        return user

    def _assign_group(self, user):
        user.groups.clear()
        group, _ = Group.objects.get_or_create(name=user.rol)
        user.groups.add(group)
