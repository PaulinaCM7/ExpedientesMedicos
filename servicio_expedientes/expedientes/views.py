from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from .models import NotaMedica
from .serializers import NotaMedicaSerializer


@api_view(['GET'])
def buscar_inseguro(request):
    try:
        nss = request.GET.get('nss')

        if not nss:
            return Response({
                'error': 'El parámetro NSS es requerido'
            }, status=status.HTTP_400_BAD_REQUEST)

        query_paciente = f"""
            SELECT id FROM pacientes_paciente WHERE nss = '{nss}'
        """

        with connection.cursor() as cursor:
            cursor.execute(query_paciente)
            paciente_row = cursor.fetchone()

        if not paciente_row:
            return Response({
                'mensaje': 'Paciente no encontrado',
                'advertencia': 'Este endpoint es vulnerable a SQL Injection'
            }, status=status.HTTP_404_NOT_FOUND)

        id_paciente = paciente_row[0]

        query_notas = f"""
            SELECT id, id_paciente, id_doctor, fecha_consulta, diagnostico, tratamiento, fecha_creacion, fecha_actualizacion
            FROM expedientes_notamedica
            WHERE id_paciente = {id_paciente}
            ORDER BY fecha_consulta DESC
        """

        with connection.cursor() as cursor:
            cursor.execute(query_notas)
            notas_rows = cursor.fetchall()

        if not notas_rows:
            return Response({
                'mensaje': 'No se encontraron notas médicas para este paciente',
                'advertencia': 'Este endpoint es vulnerable a SQL Injection',
                'id_paciente': id_paciente
            }, status=status.HTTP_404_NOT_FOUND)

        notas = []
        for row in notas_rows:
            notas.append({
                'id': row[0],
                'id_paciente': row[1],
                'id_doctor': row[2],
                'fecha_consulta': row[3],
                'diagnostico': row[4],
                'tratamiento': row[5],
                'fecha_creacion': row[6],
                'fecha_actualizacion': row[7],
            })

        return Response({
            'mensaje': 'Notas médicas encontradas (método inseguro)',
            'advertencia': 'Este endpoint es vulnerable a SQL Injection',
            'total': len(notas),
            'notas': notas
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            'error': str(e),
            'mensaje': 'Error al buscar notas médicas'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def buscar_seguro(request):
    try:
        nss = request.GET.get('nss')

        if not nss:
            return Response({
                'error': 'El parámetro NSS es requerido'
            }, status=status.HTTP_400_BAD_REQUEST)

        from django.apps import apps

        Paciente = apps.get_model('pacientes', 'Paciente')
        paciente = Paciente.objects.filter(nss=nss).first()

        if not paciente:
            return Response({
                'mensaje': 'Paciente no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)

        id_paciente = paciente.id


        notas = NotaMedica.objects.filter(id_paciente=id_paciente).order_by('-fecha_consulta')

        if not notas.exists():
            return Response({
                'mensaje': 'No se encontraron notas médicas para este paciente',
                'id_paciente': id_paciente
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = NotaMedicaSerializer(notas, many=True)

        return Response({
            'mensaje': 'Notas médicas encontradas (método seguro)',
            'total': notas.count(),
            'notas': serializer.data
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            'error': str(e),
            'mensaje': 'Error al buscar notas médicas'
        }, status=status.HTTP_400_BAD_REQUEST)