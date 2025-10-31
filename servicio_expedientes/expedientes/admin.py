from django.contrib import admin
from .models import NotaMedica


@admin.register(NotaMedica)
class NotaMedicaAdmin(admin.ModelAdmin):
    list_display = ['id', 'id_paciente', 'id_doctor', 'fecha_consulta', 'fecha_creacion']
    list_filter = ['fecha_consulta', 'fecha_creacion']
    search_fields = ['id_paciente', 'id_doctor', 'diagnostico', 'tratamiento']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    date_hierarchy = 'fecha_consulta'

    fieldsets = (
        ('Referencias', {
            'fields': ('id_paciente', 'id_doctor')
        }),
        ('Información de la Consulta', {
            'fields': ('fecha_consulta', 'diagnostico', 'tratamiento')
        }),
        ('Metadatos', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
