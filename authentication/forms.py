from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm
from .models import Usuarios
from .utils import crearUsuarioAuto
class UserLoginForm(AuthenticationForm):

    username = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'class':'form-control my-4 py-2',
                'placeholder':'Enter your username',
                'readonly':True
            }
        )
    )

    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control my-4 py-2',
                'placeholder':'Enter your password',
                'readonly':True
            }
        )
    )

    class Meta:
        model = Usuarios
        fields = ["username","password"]

class UserRegisterForm(UserCreationForm):

    new_user = crearUsuarioAuto()
    username = forms.CharField(
        label='',
        initial=new_user["username"],
        widget=forms.TextInput(
            attrs={
                'class':'form-control my-4 py-2',
                'placeholder':'Enter your username'
            }
        ),
        disabled=True,
        
    )

    password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control my-4 py-2',
                'placeholder':'Enter your password',
                'readonly':True
            }
        )
    )

    password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control my-4 py-2',
                'placeholder':'Confirm your password',
                'readonly':True
            }
        )
    )

    email = forms.CharField(
        label='',
        initial=new_user["email"],
        widget=forms.EmailInput(
            attrs={
                'class':'form-control my-4 py-2',
                'placeholder':'Email'
            }
        ),
        disabled=True
    )

    avatar = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={'id': 'avatar_input'})
    )

    class Meta:
        model = Usuarios
        fields = ["username","password1","password2","email",'avatar']

class CustomPasswordChangeForm(PasswordChangeForm):
    """
    Formulario personalizado que hereda de PasswordChangeForm.
    Usaremos esto principalmente para aplicar clases CSS (widgets)
    y personalizar los labels si es necesario.
    """
    
    # Sobrescribimos los campos para añadir widgets o personalizar labels/ayudas
    old_password = forms.CharField(
        label="Contraseña actual",
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control my-4 py-2',
                'placeholder':'Contraseña actual'
            }
        )
    )
    
    new_password1 = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control my-4 py-2',
                'placeholder':'Nueva contraseña'
            }
        )
    )
    
    new_password2 = forms.CharField(
        label="Confirmar nueva contraseña",
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control my-4 py-2',
                'placeholder':'Repetir contraseña'
            }
        )
    )

    class Meta:
        model = Usuarios
        fields = ["username","new_password1","new_password2"]