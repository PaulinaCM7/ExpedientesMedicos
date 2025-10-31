from django.contrib import admin
from .models import Paciente


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'nss', 'email', 'es_doctor', 'fecha_registro']
    list_filter = ['es_doctor', 'fecha_registro']
    search_fields = ['nombre', 'nss', 'email']
    readonly_fields = ['fecha_registro', 'fecha_actualizacion', 'password']

    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre', 'fecha_nacimiento', 'nss', 'email')
        }),
        ('Acceso', {
            'fields': ('password', 'es_doctor')
        }),
        ('Fechas', {
            'fields': ('fecha_registro', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
