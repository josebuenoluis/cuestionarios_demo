from django.urls import path
from cuestionarios import views as cuestionarios_views
from .views import LoginView,logout_view,RegisterView,AvataresView,OlvidoPasswordView,TokenAuthView,user_verified_view
urlpatterns = [
    path('login/',LoginView.as_view(),name="authentication/login"),
    path('logout/',logout_view,name='authentication/logout'),
    path('register/',RegisterView.as_view(),name="authentication/register"),
    path('avatares/',AvataresView.as_view(),name="authentication/avatares"),
    path('forgot/',OlvidoPasswordView.as_view(),name="authentication/forgot"),
    path('token/<str:tipo>/',TokenAuthView.as_view(),name="authentication/token"),
    path('verified/<str:token>/',user_verified_view,name="authentication/verified")
]