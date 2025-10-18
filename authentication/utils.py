from .models import Usuarios


def crearUsuarioAuto() -> dict:
    """Funcion para crear un usuario automaticamente"""
    user_last = Usuarios.objects.last()
    new_username = f"usuario{user_last.id+1}"
    new_email = f"prueba{user_last.id+1}@correo.com"
    return {"username":new_username,"email":new_email,"password":"pruebausuario12345678"}
