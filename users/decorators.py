from django.contrib.auth.decorators import user_passes_test


def role_required(allowed_roles):
    def check(user):
        # Allow if authenticated AND either superuser or role in allowed_roles
        if not user.is_authenticated:
            return False
        if getattr(user, 'is_superuser', False):
            return True
        return getattr(user, 'rol', None) in allowed_roles
    return user_passes_test(check)
