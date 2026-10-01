from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from .models import Perfil

# Hereda la estructura de autenticación para validar con RUT
class RutAuthBackend(BaseBackend):
    def authenticate(self, request, rut=None, password=None, **kwargs):
        if not rut or not password:
            # Si los datos están en blanco, no retorna nada
            return None

        # Limpia el RUT capturado
        rut_limpio = rut.replace('.', '').replace(' ', '').upper().strip()

        try:
            # Busca el Perfil y obtiene el user vinculado a este
            perfil = Perfil.objects.select_related('user').get(rut=rut_limpio)
            user = perfil.user
            
            # Valida la contraseña con hash del usuario de Django
            if user.check_password(password) and user.is_active:
                return user
        except Perfil.DoesNotExist:
            return None

    # Recupera la instancia del usuario con su id
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None