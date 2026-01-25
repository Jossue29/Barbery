from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group

User = get_user_model()


# ===============================
# FORM CREAR USUARIO
# ===============================
class UserCreateForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            'username',
            'nombre',
            'apellido',
            'telefono',
            'identidad',
            'direccion',
            'email',
            'rol',
        )
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'identidad': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-select'}),
        }

    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
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


# ===============================
# FORM EDITAR USUARIO
# ===============================
class UserUpdateForm(UserChangeForm):
    password = None  # 👈 elimina el campo password del formulario

    class Meta:
        model = User
        fields = (
            'username',
            'nombre',
            'apellido',
            'telefono',
            'identidad',
            'direccion',
            'email',
            'rol',
        )
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': True  # 👈 buena práctica
            }),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'identidad': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-select'}),
        }

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
