from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from .models import *
from .forms import UserLoginForm,UserRegisterForm
from django.http import JsonResponse
import json
from panel.utils import enviarCorreo
from .utils import crearUsuarioAuto


# Create your views here.

class LoginView(View):
    def get(self,request):
        form = UserLoginForm()
        if request.user.is_authenticated:
            return redirect("panel")
        else: 
            users = Usuarios.objects.filter(is_superuser=False)
            return render(request,'authentication/login.html',{"form":form,"usuarios":users})
        
    def post(self,request):

        form = UserLoginForm(request,data=request.POST)
        print("Form: ",form)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username,password=password)
            print("User: ",user)
            if user is not None:
                login(request,user)
                return redirect("cuestionarios")
            else:
                messages.error(request,'Invalid username or password')
        else:
            messages.error(request,form)
        return render(request,'authentication/login.html',{"form":form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request,'You have successfully logged out')
    return redirect('authentication/login')
    
def user_verified_view(request,token):
    try:
        token_instance = TokenChange.objects.get(token=token)
        usuario = token_instance.user_fk
        usuario.is_active = True
        usuario.save()
        token_instance.delete()
        messages.success(request, "Cuenta verificada correctamente.")
        return render(request, 'authentication/user_verified.html', {"valid": True, "username": usuario.username})
    except TokenChange.DoesNotExist:
        messages.error(request, "Token inválido o expirado.")
        return render(request, 'authentication/user_verified.html', {"valid": False})

class RegisterView(View):
    def get(self,request):
        form = UserRegisterForm()
        avatares = obtener_avatares_cache()
        new_user = crearUsuarioAuto()
        print(new_user)
        return render(request,'authentication/register.html',{"form":form,'avatares':avatares,'avatar_usuario':avatares[0],
                                                              "new_user":new_user})

    def post(self,request):
        form = UserRegisterForm(request.POST)
        print("POST FORMULARIO")
        if form.is_valid():
            user = form.save(commit=False)
            print(user)
            username = form.cleaned_data.get("username")
            password1 = form.cleaned_data.get("password1")
            user.is_active = False
            user.save()
            # Generar token con la View de Token
            token_instance = TokenChange.objects.create(user_fk=user)
            token = token_instance.token
            # user = authenticate(username=username,password=password1)
            # login(request,user)
            messages.success(request,'Registration successful')
            return render(request,'authentication/register_pending.html',{"token":token})
        else:
            messages.error(request,'Unsuccessful registration. Invalid information.')
        return render(request,'authentication/register.html',{"form":form})
    
class AvataresView(View):
    def get(self,request):
        return JsonResponse({"avatares":"obtener_avatares_cache()"})
    

class OlvidoPasswordView(View):
    def get(self,request):


        return render(request,'authentication/forgot_password.html')
    
    def post(self,request):
        try:
            data = json.loads(request.body)
        except ValueError:
            return JsonResponse({"status": False, "error": "invalid_json"}, status=400)

        email = data.get("email")
        password_new = data.get("new_password")
        if not email or not password_new:
            return JsonResponse({"status": False, "error": "missing_fields"}, status=400)

        try:
            usuario = Usuarios.objects.get(email=email)
        except Usuarios.DoesNotExist:
            return JsonResponse({"status": False, "error": "invalid_email"}, status=400)

        usuario.set_password(password_new)
        usuario.save()
        return JsonResponse({"status": True})


class TokenAuthView(View):

    def post(self,request,tipo=""):
        if tipo == "generar":
            data = json.loads(request.body)
            email = data.get('email') if data.get('email') != "" else None
            print("Email para cambio: ",email)
            usuario = Usuarios.objects.get(email=email)
            token_instance = TokenChange.objects.create(user_fk=usuario)
            token = token_instance.token
            # enviarCorreo(usuario.username,usuario.email,token_instance.token)
            print("Token generado: ",token)
            return JsonResponse({"status":True,"token":token})
        
        elif tipo == "verificar":
            data = json.loads(request.body)
            token_input = data.get('token',None)
            if token_input:
                try:
                    token_instance = TokenChange.objects.get(token=token_input)
                    print("Token verificado: ",token_instance.token)
                    return JsonResponse({"status":True})
                except TokenChange.DoesNotExist:
                    print("Token no existente")
                    return JsonResponse({"status":False})
        return JsonResponse({"status":""})
    