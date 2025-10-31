from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import MinLengthValidator, MaxLengthValidator


class Paciente(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="Nombre completo")
    fecha_nacimiento = models.DateField(verbose_name="Fecha de nacimiento")
    nss = models.CharField(
        max_length=11,
        validators=[MinLengthValidator(11), MaxLengthValidator(11)],
        unique=True,
        verbose_name="Número de Seguridad Social",
        help_text="Debe contener exactamente 11 dígitos"
    )
    email = models.EmailField(unique=True, verbose_name="Correo electrónico")
    password = models.CharField(max_length=255, verbose_name="Contraseña")
    es_doctor = models.BooleanField(
        default=False,
        verbose_name="¿Es doctor?"
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        ordering = ['-fecha_registro']

    def __str__(self):
        rol = "Doctor" if self.es_doctor else "Paciente"
        return f"{self.nombre} ({rol}) - NSS: {self.nss}"

    def set_password(self, raw_password):
        """Hashea la contraseña antes de guardarla"""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Verifica si la contraseña es correcta"""
        return check_password(raw_password, self.password)
