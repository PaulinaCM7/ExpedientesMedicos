from rest_framework import serializers
from .models import Paciente


class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = ['id', 'nombre', 'fecha_nacimiento', 'nss', 'email', 'password', 'es_doctor', 'fecha_registro', 'fecha_actualizacion']
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True},
            'fecha_registro': {'read_only': True},
            'fecha_actualizacion': {'read_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        paciente = Paciente(**validated_data)
        paciente.set_password(password)
        paciente.save()
        return paciente

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
