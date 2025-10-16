from django.urls import path
from .views import PanelView,TokenChangeView,PasswordChangeView

urlpatterns = [
    path('',PanelView.as_view(),name="panel"),
    path('guardar/<str:tipo>/',PanelView.as_view(),name="panel/guardar"),
    path('token/<str:tipo>/',TokenChangeView.as_view(),name="panel/token"),
    path('form/password/',PasswordChangeView.as_view(),name="panel/password"),
]