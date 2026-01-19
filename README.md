# Barbería - Sistema de Facturación (Django)

Instrucciones rápidas:

- Crear y activar un virtualenv

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

- Migrar y crear superusuario

```bash
python manage.py migrate
python manage.py createsuperuser
```

- Ejecutar servidor

```bash
python manage.py runserver
```

Endpoints principales:

- `/login/` - Iniciar sesión
- `/` - Dashboard
- `/facturacion/crear/` - Crear factura (AJAX)
- `/facturacion/ticket/<id>/` - Vista de impresión

Notas:

- Archivo `barberia/settings.py` contiene la configuración básica. Reemplaza `SECRET_KEY` en producción.
- Modelo de usuario personalizado: `users.models.User`.
