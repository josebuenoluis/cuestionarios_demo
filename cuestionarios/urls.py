from django.urls import path
from cuestionarios import views as cuestionarios_views
from .views import CuestionariosView,CrearCuestionarioView,ContestarCuestionarioView
urlpatterns = [
    path('',CuestionariosView.as_view(),name="cuestionarios"),
    path('<int:n_pagina>',CuestionariosView.as_view(),name="cuestionarios"),
    path('crear',CrearCuestionarioView.as_view(),name="crear_cuestionario"),
    path('contestar/<int:cuestionario_id>',ContestarCuestionarioView.as_view(),name="contestar_cuestionario"),
]