from django.shortcuts import render
from django.views import View
from .utils import obtener_avatares_cache
from django.http import JsonResponse
from authentication.models import TokenChange,Usuarios
from authentication.forms import PasswordChangeForm
from django.contrib.auth import login,authenticate,logout
from .utils import enviarCorreo
# Create your views here.
import json

class PanelView(View):
    def get(self,request):

        nombre_usuario = request.user.username
        # avatar = request.user.avatar.url if request.user.avatar else None
        email = request.user.email
        avatares = obtener_avatares_cache()
        print(nombre_usuario)
        print(request.user.email)
        return render(request,'panel/panel.html',{"nombre_usuario":nombre_usuario,'email':email,'avatares':avatares,"avatar_usuario":request.user.avatar})

    def post(self,request,tipo=""):
        print("Tipo: ",tipo)
        if tipo == "avatar":
            data = json.loads(request.body)
            avatar_seleccionado = data.get('avatar',None)
            print("dentro de avatar: ",avatar_seleccionado)
            if avatar_seleccionado:
                print("dentro de avatar guardando")
                usuario = request.user
                usuario.avatar = avatar_seleccionado
                usuario.save()
                return JsonResponse({"status":True})
        elif tipo == "username":
            data = json.loads(request.body)
            username_nuevo = data.get('username',None)
            if username_nuevo:
                usuario = request.user
                usuario.username = username_nuevo
                usuario.save()
                return JsonResponse({"status":True})
        elif tipo == "email":
            data = json.loads(request.body)
            email_nuevo = data.get('email',None)
            if email_nuevo:
                usuario = request.user
                usuario.email = email_nuevo
                usuario.save()
                return JsonResponse({"status":True})
        elif tipo == "password":
            data = json.loads(request.body)
            password_old = data.get('old_password',None)
            password_nuevo = data.get('new_password',None)
            validar_password = Usuarios.check_password(request.user,password_old)
            if validar_password and password_nuevo:
                usuario = request.user
                usuario.set_password(password_nuevo)
                usuario.save()
                user_auth = authenticate(username=usuario,password=password_nuevo)
                login(request,user_auth)
                return JsonResponse({"status":True})
            else:
                return JsonResponse({"status":False})

            # if password_old:
            #     usuario = request.user
            #     usuario.set_password(password_nuevo)
            #     usuario.save()
        return JsonResponse({"status":""})
    
class TokenChangeView(View):

    def post(self,request,tipo=""):
        if tipo == "generar":
            data = json.loads(request.body)
            email = data.get('email') if data.get('email') != "" else request.user.email
            print("Email para cambio: ",email)
            usuario = request.user
            token_instance = TokenChange.objects.create(user_fk=usuario)
            token = token_instance.token
            enviarCorreo(request.user.username,email,token_instance.token)
            print("Token generado: ",token)
            return JsonResponse({"status":True})
        
        elif tipo == "verificar":
            data = json.loads(request.body)
            token_input = data.get('token',None)
            if token_input:
                try:
                    token_instance = TokenChange.objects.get(token=token_input,user_fk=request.user)
                    print("Token verificado: ",token_instance.token)
                    return JsonResponse({"status":True})
                except TokenChange.DoesNotExist:
                    print("Token no existente")
                    return JsonResponse({"status":False})
        return JsonResponse({"status":""})
    
class PasswordChangeView(View):
    def get(self,request):
        form = PasswordChangeForm(user=request.user)
        return render(request,'panel/change_password.html',{'form':form})