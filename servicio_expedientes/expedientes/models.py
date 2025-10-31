from django.db import models


class NotaMedica(models.Model):
    id_paciente = models.IntegerField(
        verbose_name="ID del Paciente",
        help_text="ID del paciente en el microservicio de pacientes",
        db_index=True
    )
    id_doctor = models.IntegerField(
        verbose_name="ID del Doctor",
        help_text="ID del doctor en el microservicio de pacientes",
        db_index=True
    )
    fecha_consulta = models.DateTimeField(
        verbose_name="Fecha y hora de la consulta",
        db_index=True
    )
    diagnostico = models.TextField(
        verbose_name="Diagnóstico",
        help_text="Diagnóstico médico del paciente"
    )
    tratamiento = models.TextField(
        verbose_name="Tratamiento",
        help_text="Tratamiento prescrito al paciente"
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación del registro"
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de última actualización"
    )

    class Meta:
        verbose_name = "Nota Médica"
        verbose_name_plural = "Notas Médicas"
        ordering = ['-fecha_consulta']
        indexes = [
            models.Index(fields=['id_paciente', '-fecha_consulta']),
            models.Index(fields=['id_doctor', '-fecha_consulta']),
        ]

    def __str__(self):
        return f"Nota #{self.id} - Paciente: {self.id_paciente} - Doctor: {self.id_doctor} - {self.fecha_consulta.strftime('%Y-%m-%d')}"
