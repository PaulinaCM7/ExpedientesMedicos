from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from django.contrib.auth.hashers import make_password
from .serializers import PacienteSerializer
from .models import Paciente


@api_view(['POST'])
def registro_inseguro(request):
    try:
        nombre = request.data.get('nombre')
        fecha_nacimiento = request.data.get('fecha_nacimiento')
        nss = request.data.get('nss')
        email = request.data.get('email')
        password = request.data.get('password')
        es_doctor = request.data.get('es_doctor', False)

        hashed_password = make_password(password)

        query = f"""
            INSERT INTO pacientes_paciente
            (nombre, fecha_nacimiento, nss, email, password, es_doctor, fecha_registro, fecha_actualizacion)
            VALUES ('{nombre}', '{fecha_nacimiento}', '{nss}', '{email}', '{hashed_password}', {es_doctor}, datetime('now'), datetime('now'))
        """

        with connection.cursor() as cursor:
            cursor.execute(query)

        return Response({
            'mensaje': 'Paciente registrado exitosamente (método inseguro)',
            'advertencia': 'Este endpoint es vulnerable a SQL Injection',
            'datos': {
                'nombre': nombre,
                'email': email,
                'nss': nss,
                'es_doctor': es_doctor
            }
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({
            'error': str(e),
            'mensaje': 'Error al registrar paciente'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def registro_seguro(request):
    serializer = PacienteSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        return Response({
            'mensaje': 'Paciente registrado exitosamente (método seguro)',
            'datos': serializer.data
        }, status=status.HTTP_201_CREATED)

    return Response({
        'error': serializer.errors,
        'mensaje': 'Error de validación'
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def perfil_inseguro(request, id):
    try:
        nombre = request.data.get('nombre')
        fecha_nacimiento = request.data.get('fecha_nacimiento')
        nss = request.data.get('nss')
        email = request.data.get('email')

        query = f"""
            UPDATE pacientes_paciente
            SET nombre = '{nombre}',
                fecha_nacimiento = '{fecha_nacimiento}',
                nss = '{nss}',
                email = '{email}',
                fecha_actualizacion = datetime('now')
            WHERE id = {id}
        """

        with connection.cursor() as cursor:
            cursor.execute(query)

        return Response({
            'mensaje': 'Perfil actualizado exitosamente (método inseguro)',
            'advertencia': 'Este endpoint es vulnerable a SQL Injection',
            'datos': {
                'id': id,
                'nombre': nombre,
                'email': email,
                'nss': nss
            }
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            'error': str(e),
            'mensaje': 'Error al actualizar perfil'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def perfil_seguro(request, id):
    try:
        paciente = Paciente.objects.get(id=id)
    except Paciente.DoesNotExist:
        return Response({
            'mensaje': 'Paciente no encontrado'
        }, status=status.HTTP_404_NOT_FOUND)

    serializer = PacienteSerializer(paciente, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

        return Response({
            'mensaje': 'Perfil actualizado exitosamente (método seguro)',
            'datos': serializer.data
        }, status=status.HTTP_200_OK)

    return Response({
        'error': serializer.errors,
        'mensaje': 'Error de validación'
    }, status=status.HTTP_400_BAD_REQUEST)
