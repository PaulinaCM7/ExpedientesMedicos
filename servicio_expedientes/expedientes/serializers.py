from rest_framework import serializers
from .models import NotaMedica


class NotaMedicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotaMedica
        fields = ['id', 'id_paciente', 'id_doctor', 'fecha_consulta', 'diagnostico', 'tratamiento', 'fecha_creacion', 'fecha_actualizacion']
        extra_kwargs = {
            'id': {'read_only': True},
            'fecha_creacion': {'read_only': True},
            'fecha_actualizacion': {'read_only': True},
        }

    def validate_id_paciente(self, value):
        if value <= 0:
            raise serializers.ValidationError("El ID del paciente debe ser un número positivo.")
        return value

    def validate_id_doctor(self, value):
        if value <= 0:
            raise serializers.ValidationError("El ID del doctor debe ser un número positivo.")
        return value
