from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from facturacion.models import Factura
from datetime import datetime


class FacturaModelTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='admin', password='1234')
        # aquí puedes crear más objetos relacionados si es necesario

    def test_crear_factura(self):
        factura = Factura.objects.create(
            cliente_nombre='Juan Perez',
            total_factura=500,
            fecha=datetime.now(),
            creado_por=self.user
        )
        self.assertEqual(factura.total_factura, 500)
        self.assertEqual(factura.cliente_nombre, 'Juan Perez')

class DashboardViewTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='admin', password='1234')
        self.client = Client()

    def test_dashboard_login_required(self):
        # sin login, debe redirigir
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)  # redirige a login

    def test_dashboard_loads(self):
        # con login
        self.client.login(username='admin', password='1234')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertContains(response, 'Ingresos de la semana')

from users.forms import PerfilForm

class PerfilFormTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='admin', password='1234')

    def test_form_valido(self):
        form_data = {
            'nombre': 'Bladimir',
            'apellido': 'Gonzalez',
            'email': 'bladimir@example.com',
            'telefono': '12345678',
            'direccion': 'Mi dirección'
        }
        form = PerfilForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_form_invalido_email_repetido(self):
        User = get_user_model()
        User.objects.create_user(username='otro', email='email@ejemplo.com', password='1234')
        form_data = {
            'nombre': 'Bladimir',
            'apellido': 'Gonzalez',
            'email': 'email@ejemplo.com',  # repetido
            'telefono': '12345678',
            'direccion': 'Mi dirección'
        }
        form = PerfilForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
