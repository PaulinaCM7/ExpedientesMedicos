from django.urls import path
from . import views

urlpatterns = [
    path('inseguro/registro', views.registro_inseguro, name='registro_inseguro'),
    path('seguro/registro', views.registro_seguro, name='registro_seguro'),
]
