from functools import wraps
from django.shortcuts import redirect

# Crea un decorador (cambia el comportamiento de una vista sin cambiar el código) personalizado que envuelve (wrap) una vista para protegerla
def usuario_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Verifica si usuario_id existe en la sesion actual, con tal de no tener que volver a ingresar las credenciales
        if 'usuario_id' not in request.session:
            # Si no existe, redirige a la página de inicio de sesión
            return redirect('login')
        # Si se autenticó el usuario en la sesión, ejecuta la vista original
        return view_func(request, *args, **kwargs)
    return _wrapped_view