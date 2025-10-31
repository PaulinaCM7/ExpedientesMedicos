from django.urls import path
from . import views

urlpatterns = [
    path('inseguro/registro', views.registro_inseguro, name='registro_inseguro'),
    path('seguro/registro', views.registro_seguro, name='registro_seguro'),
    path('inseguro/perfil/<int:id>', views.perfil_inseguro, name='perfil_inseguro'),
    path('seguro/perfil/<int:id>', views.perfil_seguro, name='perfil_seguro'),
]
