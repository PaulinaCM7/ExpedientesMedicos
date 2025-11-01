from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import connection, connections
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

        query_paciente = f"SELECT id FROM pacientes_paciente WHERE nss = '{nss}'"
        
        with connections['pacientes_db'].cursor() as cursor:
            cursor.execute(query_paciente)
            pacientes = cursor.fetchall()

        if not pacientes:
            return Response({
                'mensaje': 'Paciente no encontrado',
                'advertencia': 'Este endpoint es vulnerable a SQL Injection'
            }, status=status.HTTP_404_NOT_FOUND)

        id_paciente = None
        for paciente in pacientes:
            paciente_id = paciente[0]
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT 1 FROM expedientes_notamedica WHERE id_paciente = {paciente_id} LIMIT 1")
                if cursor.fetchone():
                    id_paciente = paciente_id
                    break
        
        if not id_paciente:
            return Response({
                'mensaje': 'Ninguno de los pacientes encontrados tiene notas médicas',
                'pacientes_encontrados': [p[0] for p in pacientes],
                'advertencia': 'Este endpoint es vulnerable a SQL Injection'
            }, status=status.HTTP_404_NOT_FOUND)

        query_notas = f"SELECT * FROM expedientes_notamedica WHERE id_paciente = {id_paciente}"
        
        with connection.cursor() as cursor:
            cursor.execute(query_notas)
            notas_rows = cursor.fetchall()

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
            'id_paciente_usado': id_paciente,
            'pacientes_encontrados': [p[0] for p in pacientes],
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

        with connections['pacientes_db'].cursor() as cursor:
            cursor.execute(
                "SELECT id FROM pacientes_paciente WHERE nss = %s",
                [nss]
            )
            paciente_row = cursor.fetchone()

        if not paciente_row:
            return Response({
                'mensaje': 'Paciente no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)

        id_paciente = paciente_row[0]

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


@api_view(['POST'])
def crear_inseguro(request):
    try:
        id_paciente = request.data.get('id_paciente')
        id_doctor = request.data.get('id_doctor')
        fecha_consulta = request.data.get('fecha_consulta')
        diagnostico = request.data.get('diagnostico')
        tratamiento = request.data.get('tratamiento')

        query = f"""
            INSERT INTO expedientes_notamedica
            (id_paciente, id_doctor, fecha_consulta, diagnostico, tratamiento, fecha_creacion, fecha_actualizacion)
            VALUES ({id_paciente}, {id_doctor}, '{fecha_consulta}', '{diagnostico}', '{tratamiento}', datetime('now'), datetime('now'))
        """

        with connection.cursor() as cursor:
            cursor.execute(query)
            nota_id = cursor.lastrowid

        return Response({
            'mensaje': 'Nota médica creada exitosamente (método inseguro)',
            'advertencia': 'Este endpoint es vulnerable a SQL Injection y Asignación Masiva',
            'datos': {
                'id': nota_id,
                'id_paciente': id_paciente,
                'id_doctor': id_doctor,
                'fecha_consulta': fecha_consulta,
                'diagnostico': diagnostico,
                'tratamiento': tratamiento
            }
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({
            'error': str(e),
            'mensaje': 'Error al crear nota médica'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def crear_seguro(request):
    serializer = NotaMedicaSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        return Response({
            'mensaje': 'Nota médica creada exitosamente (método seguro)',
            'datos': serializer.data
        }, status=status.HTTP_201_CREATED)

    return Response({
        'error': serializer.errors,
        'mensaje': 'Error de validación'
    }, status=status.HTTP_400_BAD_REQUEST)