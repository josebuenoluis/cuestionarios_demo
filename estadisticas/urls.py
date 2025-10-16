from django.urls import path
from estadisticas import views as estadisticas_views
from .views import EstadisticasView,EstadisticasGeneralesView
urlpatterns = [
    path('',EstadisticasView.as_view(),name="estadisticas"),
    path('<str:tipo>/',EstadisticasGeneralesView.as_view(),name="general")
]