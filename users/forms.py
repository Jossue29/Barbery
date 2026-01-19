from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

User = get_user_model()


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'nombre', 'apellido', 'telefono', 'identidad', 'direccion', 'email', 'rol')


class UserUpdateForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ('username', 'nombre', 'apellido', 'telefono', 'identidad', 'direccion', 'email', 'rol')
