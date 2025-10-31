from django.urls import path
from . import views

urlpatterns = [
    path('inseguro/buscar', views.buscar_inseguro, name='buscar_inseguro'),
    path('seguro/buscar', views.buscar_seguro, name='buscar_seguro'),
    path('inseguro/crear', views.crear_inseguro, name='crear_inseguro'),
    path('seguro/crear', views.crear_seguro, name='crear_seguro'),
]
