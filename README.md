# Sistema de Expedientes Médicos Simplificado (API REST)

## 📖 Introducción

El **Sistema de Expedientes Médicos** es una aplicación backend desarrollada con **Django REST Framework** que simula la gestión de expedientes clínicos en una institución de salud. El proyecto implementa una **arquitectura de microservicios** con dos servicios independientes que manejan la información de pacientes y sus historiales médicos.

### Propósito Educativo

Este proyecto tiene un **propósito estrictamente educativo** y demuestra de manera práctica:

- **Vulnerabilidades críticas de seguridad**: SQL Injection y Asignación Masiva
- **Comparación de código seguro vs. inseguro**: Cada endpoint crítico tiene dos versiones
- **Importancia del uso de ORMs**: Django ORM como capa de abstracción y seguridad
- **Validación y sanitización de datos**: Uso de serializadores de Django REST Framework
- **Mejores prácticas en desarrollo de APIs REST**: Arquitectura de microservicios, manejo de errores, y respuestas estandarizadas

El sistema maneja dos tipos de roles:
- **DOCTOR**: Puede crear y consultar notas médicas
- **PACIENTE**: Puede consultar sus propios expedientes médicos

---

## 🏗️ Arquitectura del Sistema

El proyecto implementa una arquitectura de **microservicios** con dos servicios independientes:

```
┌─────────────────────────────────────────────────────────┐
│                     CLIENTE                              │
│         (Web App / Mobile App / Postman)                │
└───────────────────┬─────────────────────────────────────┘
                    │
        ┌───────────┴────────────┐
        │                        │
┌───────▼──────────┐    ┌───────▼───────────┐
│   SERVICIO DE    │    │   SERVICIO DE     │
│   PACIENTES      │    │   EXPEDIENTES     │
│   (Puerto 8000)  │    │   (Puerto 8001)   │
├──────────────────┤    ├───────────────────┤
│ • Registro       │    │ • Crear Notas     │
│ • Actualización  │    │ • Buscar Notas    │
│ • Gestión Perfil │    │ • Consultas       │
└────────┬─────────┘    └─────────┬─────────┘
         │                        │
    ┌────▼────┐              ┌────▼────┐
    │SQLite DB│              │SQLite DB│
    │pacientes│              │notas    │
    └─────────┘              └─────────┘
```

### Microservicio 1: Servicio de Pacientes
- **Responsabilidad**: Gestión de datos personales de pacientes y doctores
- **Base de datos**: `pacientes_paciente` (SQLite)
- **Puerto**: 8000
- **Modelo de Datos**: Paciente (id, nombre, fecha_nacimiento, nss, email, password, es_doctor)

### Microservicio 2: Servicio de Expedientes
- **Responsabilidad**: Gestión de notas médicas y expedientes clínicos
- **Base de datos**: `expedientes_notamedica` (SQLite)
- **Puerto**: 8001
- **Modelo de Datos**: NotaMedica (id, id_paciente, id_doctor, fecha_consulta, diagnostico, tratamiento)

---

## 🚀 Instrucciones para Levantar el Entorno

### Requisitos Previos

- **Python** 3.8 o superior
- **pip** (gestor de paquetes de Python)
- **Git**
- **Postman** o **Insomnia** (opcional, para probar endpoints)
- **Virtual environment** (recomendado)

### 1. Clonar el repositorio

```bash
git clone https://github.com/PaulinaCM7/ExpedientesMedicos.git
cd ExpedientesMedicos
```

### 2. Crear entorno virtual (recomendado)

```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias

#### Servicio de Pacientes
```bash
cd servicio_pacientes
pip install -r requirements.txt
```

#### Servicio de Expedientes
```bash
cd ../servicio_expedientes
pip install -r requirements.txt
```

### 4. Aplicar migraciones

#### Servicio de Pacientes
```bash
cd servicio_pacientes
python manage.py makemigrations
python manage.py migrate
```

#### Servicio de Expedientes
```bash
cd ../servicio_expedientes
python manage.py makemigrations
python manage.py migrate
```

### 5. Crear superusuario (opcional)

Para acceder al panel de administración de Django:

```bash
# En servicio_pacientes
python manage.py createsuperuser

# En servicio_expedientes
python manage.py createsuperuser
```

### 6. Ejecución de los Servicios

Necesitas **dos terminales** para ejecutar ambos servicios simultáneamente:

#### Terminal 1: Servicio de Pacientes
```bash
cd servicio_pacientes
python manage.py runserver 8000
```

#### Terminal 2: Servicio de Expedientes
```bash
cd servicio_expedientes
python manage.py runserver 8001
```

### 7. Verificar que los servicios están funcionando

- Servicio de Pacientes: http://localhost:8000/admin/
- Servicio de Expedientes: http://localhost:8001/admin/

---

## 🔍 Análisis de Vulnerabilidades

Este proyecto implementa intencionalmente vulnerabilidades críticas de seguridad para demostrar su funcionamiento y las técnicas de mitigación correspondientes.

---

## 1️⃣ Análisis del Endpoint de Búsqueda de Expedientes

### 🔴 Controlador INSEGURO (`/inseguro/buscar`)

**Archivo**: `servicio_expedientes/expedientes/views.py:10-79`

```python
@api_view(['GET'])
def buscar_inseguro(request):
    try:
        nss = request.GET.get('nss')

        if not nss:
            return Response({
                'error': 'El parámetro NSS es requerido'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 🔴 VULNERABILIDAD: Concatenación directa de strings en SQL query
        query_paciente = f"SELECT id FROM pacientes_paciente WHERE nss = '{nss}'"

        with connections['pacientes_db'].cursor() as cursor:
            cursor.execute(query_paciente)  # 🔴 Sin sanitización
            pacientes = cursor.fetchall()

        if not pacientes:
            return Response({
                'mensaje': 'Paciente no encontrado',
                'advertencia': 'Este endpoint es vulnerable a SQL Injection'
            }, status=status.HTTP_404_NOT_FOUND)

        # ... resto del código

        # 🔴 VULNERABILIDAD: Otra query vulnerable
        query_notas = f"SELECT * FROM expedientes_notamedica WHERE id_paciente = {id_paciente}"

        with connection.cursor() as cursor:
            cursor.execute(query_notas)
            notas_rows = cursor.fetchall()

        # ... construcción manual de respuesta
```

### 🚨 Explicación de la Vulnerabilidad: SQL Injection

**SQL Injection** es una de las vulnerabilidades más críticas en aplicaciones web (OWASP Top 10). Ocurre cuando los datos proporcionados por el usuario se concatenan directamente en queries SQL sin sanitización ni validación.

#### ¿Por qué es vulnerable este código?

1. **Concatenación directa**: La línea 19 usa f-strings para construir la query:
   ```python
   query_paciente = f"SELECT id FROM pacientes_paciente WHERE nss = '{nss}'"
   ```

2. **Sin validación**: El parámetro `nss` se toma directamente de `request.GET.get('nss')` sin ninguna sanitización.

3. **Ejecución directa**: La query se ejecuta con `cursor.execute(query_paciente)` sin parámetros separados.

#### ¿Qué puede hacer un atacante?

Un atacante puede modificar la lógica de la consulta SQL inyectando código malicioso en el parámetro `nss`:

- **Extraer todos los registros**
- **Modificar datos**
- **Eliminar tablas** (limitado en SQLite)
- **Eludir autenticación**
- **Acceder a información confidencial**

### 💣 Petición en Postman que Explota la Vulnerabilidad

#### Ataque 1: Obtener TODOS los Expedientes

**Endpoint**:
```
GET http://localhost:8001/api/expedientes/inseguro/buscar?nss=123' OR '1'='1
```

**Cómo funciona:**

La query original era:
```sql
SELECT id FROM pacientes_paciente WHERE nss = '123'
```

Con el ataque, se convierte en:
```sql
SELECT id FROM pacientes_paciente WHERE nss = '123' OR '1'='1'
```

Como `'1'='1'` **siempre es verdadero**, la condición WHERE se vuelve inútil y la query devuelve **TODOS** los pacientes de la base de datos.

**Respuesta del servidor**:
```json
{
    "mensaje": "Notas médicas encontradas (método inseguro)",
    "advertencia": "Este endpoint es vulnerable a SQL Injection",
    "total": 15,
    "pacientes_encontrados": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    "notas": [
        {
            "id": 1,
            "id_paciente": 1,
            "id_doctor": 2,
            "diagnostico": "Información confidencial del paciente...",
            "tratamiento": "..."
        },
        // ... más notas de otros pacientes
    ]
}
```

#### Ataque 2: SQL Injection con Comentarios

**Endpoint**:
```
GET http://localhost:8001/api/expedientes/inseguro/buscar?nss=123' --
```

**Cómo funciona:**

La query se convierte en:
```sql
SELECT id FROM pacientes_paciente WHERE nss = '123' --'
```

El `--` comenta el resto de la query, eliminando la comilla final y cualquier condición adicional.

#### Ataque 3: Always True (variante)

**Endpoint**:
```
GET http://localhost:8001/api/expedientes/inseguro/buscar?nss=' OR 1=1 OR ''='
```

**Cómo funciona:**

La query se convierte en:
```sql
SELECT id FROM pacientes_paciente WHERE nss = '' OR 1=1 OR ''=''
```

Como `1=1` es siempre verdadero, retorna todos los registros.

### ✅ Controlador SEGURO (`/seguro/buscar`)

**Archivo**: `servicio_expedientes/expedientes/views.py:82-126`

```python
@api_view(['GET'])
def buscar_seguro(request):
    try:
        nss = request.GET.get('nss')

        if not nss:
            return Response({
                'error': 'El parámetro NSS es requerido'
            }, status=status.HTTP_400_BAD_REQUEST)

        # ✅ SEGURO: Uso de parámetros parametrizados
        with connections['pacientes_db'].cursor() as cursor:
            cursor.execute(
                "SELECT id FROM pacientes_paciente WHERE nss = %s",
                [nss]  # ✅ Parámetro separado, sanitizado automáticamente
            )
            paciente_row = cursor.fetchone()

        if not paciente_row:
            return Response({
                'mensaje': 'Paciente no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)

        id_paciente = paciente_row[0]

        # ✅ SEGURO: Uso del ORM de Django
        notas = NotaMedica.objects.filter(id_paciente=id_paciente).order_by('-fecha_consulta')

        if not notas.exists():
            return Response({
                'mensaje': 'No se encontraron notas médicas para este paciente',
                'id_paciente': id_paciente
            }, status=status.HTTP_404_NOT_FOUND)

        # ✅ SEGURO: Uso de serializador para respuesta consistente
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
```

### 🛡️ ¿Cómo el ORM y los Parámetros Parametrizados Previenen el Ataque?

#### 1. **Parámetros Parametrizados (Líneas 93-96)**

```python
cursor.execute(
    "SELECT id FROM pacientes_paciente WHERE nss = %s",
    [nss]  # Parámetro separado
)
```

**Ventajas**:
- El parámetro `nss` se pasa como un **argumento separado**, no concatenado en el string SQL
- El driver de la base de datos **escapa automáticamente** caracteres especiales
- Los valores se tratan como **datos literales**, nunca como código SQL ejecutable
- **Imposible inyectar código SQL** porque el parámetro se trata como un valor, no como sintaxis

**Comparación**:

| Método Inseguro | Método Seguro |
|----------------|---------------|
| `f"... WHERE nss = '{nss}'"` | `"... WHERE nss = %s", [nss]` |
| String concatenado | Parámetro separado |
| No sanitizado | Sanitizado automáticamente |
| Vulnerable | Seguro |

#### 2. **Uso del ORM de Django (Línea 106)**

```python
notas = NotaMedica.objects.filter(id_paciente=id_paciente).order_by('-fecha_consulta')
```

**Ventajas del ORM**:
- **Abstracción completa**: No escribes SQL directamente
- **Sanitización automática**: Django genera queries parametrizadas internamente
- **Validación de tipos**: Los campos del modelo tienen tipos definidos
- **Protección contra inyecciones**: El ORM nunca interpreta los valores como código SQL
- **Mantenibilidad**: Código más legible y fácil de mantener

**Ejemplo interno**: El ORM genera internamente:
```sql
SELECT * FROM expedientes_notamedica WHERE id_paciente = %s ORDER BY fecha_consulta DESC
```
Con el parámetro `id_paciente` escapado y sanitizado automáticamente.

#### 3. **Uso de Serializadores (Línea 114)**

```python
serializer = NotaMedicaSerializer(notas, many=True)
```

**Ventajas**:
- **Validación de salida**: Solo se exponen los campos definidos en el serializador
- **Consistencia**: Respuestas estandarizadas y predecibles
- **Seguridad adicional**: Campos sensibles pueden marcarse como `write_only`

### 📊 Comparación de Resultados

| Aspecto | Endpoint Inseguro | Endpoint Seguro |
|---------|-------------------|-----------------|
| **Query con NSS válido** | Funciona, pero vulnerable | Funciona de forma segura |
| **Query con `' OR '1'='1`** | 🔴 Retorna TODOS los registros | ✅ Error o sin resultados |
| **Query con `' --`** | 🔴 Ignora validaciones | ✅ Busca literal `' --` (sin match) |
| **Query con `'; DROP TABLE`** | 🟡 Bloqueado por SQLite* | ✅ Bloqueado |
| **Riesgo de seguridad** | 🔴 CRÍTICO | ✅ MÍNIMO |

*Nota: SQLite bloquea múltiples sentencias en `execute()` por diseño, pero en MySQL/PostgreSQL este ataque funcionaría en el código inseguro.

---

## 2️⃣ Análisis del Endpoint de Registro/Actualización de Perfil

### 🔴 Controlador INSEGURO (`/inseguro/perfil`)

**Archivo**: `servicio_pacientes/pacientes/views.py:67-101`

```python
@api_view(['PUT'])
def perfil_inseguro(request, id):
    try:
        nombre = request.data.get('nombre')
        email = request.data.get('email')
        es_doctor = request.data.get('es_doctor', False)  # 🔴 VULNERABILIDAD

        # 🔴 VULNERABILIDAD: SQL Injection + Asignación Masiva
        query = f"""
            UPDATE pacientes_paciente
            SET nombre = '{nombre}',
                email = '{email}',
                es_doctor = {1 if es_doctor else 0},
                fecha_actualizacion = datetime('now')
            WHERE id = {id}
        """

        with connection.cursor() as cursor:
            cursor.execute(query)  # 🔴 Sin sanitización

        return Response({
            'mensaje': 'Perfil actualizado exitosamente (método inseguro)',
            'advertencia': 'Este endpoint es vulnerable a SQL Injection y Asignación Masiva',
            'datos': {
                'id': id,
                'nombre': nombre,
                'email': email,
                'es_doctor': es_doctor  # 🔴 Campo privilegiado modificado
            }
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            'error': str(e),
            'mensaje': 'Error al actualizar perfil'
        }, status=status.HTTP_400_BAD_REQUEST)
```

### 🚨 Explicación de la Vulnerabilidad: Asignación Masiva (Mass Assignment)

**Asignación Masiva** es una vulnerabilidad que ocurre cuando una aplicación permite que los usuarios modifiquen campos de una base de datos que **no deberían ser accesibles** directamente, aprovechando que el backend acepta cualquier parámetro sin filtrar.

#### ¿Por qué es vulnerable este código?

1. **Acepta todos los parámetros sin filtrar** (líneas 70-72):
   ```python
   nombre = request.data.get('nombre')
   email = request.data.get('email')
   es_doctor = request.data.get('es_doctor', False)  # ❌ Campo privilegiado
   ```

2. **No valida permisos**: Cualquier usuario puede enviar `es_doctor=True` y el sistema lo acepta sin verificar si tiene autorización para cambiar ese campo.

3. **Actualiza directamente en SQL**: Todos los campos enviados se actualizan sin restricciones:
   ```python
   SET nombre = '{nombre}',
       email = '{email}',
       es_doctor = {1 if es_doctor else 0},  # ❌ Campo crítico sin protección
   ```

#### ¿Qué puede hacer un atacante?

Un atacante puede:
- **Elevación de privilegios**: Convertirse en doctor sin autorización
- **Modificar campos protegidos**: Cambiar `es_doctor`, `id`, `fecha_registro`, etc.
- **Eludir controles de negocio**: Saltarse validaciones y permisos
- **Modificar datos de otros usuarios**: Si combina con SQL Injection

### 💣 Petición en Postman que Explota la Vulnerabilidad

#### Ataque: Convertirse en Doctor sin Autorización

**Endpoint**:
```
PUT http://localhost:8000/api/pacientes/inseguro/perfil/5
Content-Type: application/json
```

**Body (JSON)**:
```json
{
    "nombre": "Juan Pérez",
    "email": "juan.perez@example.com",
    "es_doctor": true
}
```

**Cómo funciona:**

1. El usuario con ID 5 es un **paciente normal** (`es_doctor = false`)
2. Envía una petición PUT con el campo `es_doctor: true`
3. El endpoint **no valida** si el usuario tiene permiso para cambiar ese campo
4. La query SQL actualiza directamente:
   ```sql
   UPDATE pacientes_paciente
   SET nombre = 'Juan Pérez',
       email = 'juan.perez@example.com',
       es_doctor = 1,  -- ❌ Cambiado a 1 (true)
       fecha_actualizacion = datetime('now')
   WHERE id = 5
   ```
5. El usuario ahora tiene **privilegios de doctor** sin autorización

**Respuesta del servidor**:
```json
{
    "mensaje": "Perfil actualizado exitosamente (método inseguro)",
    "advertencia": "Este endpoint es vulnerable a SQL Injection y Asignación Masiva",
    "datos": {
        "id": 5,
        "nombre": "Juan Pérez",
        "email": "juan.perez@example.com",
        "es_doctor": true  // ✅ Atacante ahora es "doctor"
    }
}
```

#### Impacto de la Vulnerabilidad

| Escenario | Consecuencia |
|-----------|--------------|
| **Usuario normal → Doctor** | Puede acceder a funcionalidades restringidas |
| **Modificar otros campos** | Podría cambiar `id`, `nss`, etc. si se aceptan |
| **Elusión de auditoría** | Puede manipular `fecha_registro` u otros metadatos |
| **Escalada de privilegios** | Acceso no autorizado a información sensible |

### ✅ Controlador SEGURO (`/seguro/perfil`)

**Archivo**: `servicio_pacientes/pacientes/views.py:104-126`

```python
@api_view(['PUT'])
def perfil_seguro(request, id):
    try:
        # ✅ SEGURO: ORM para obtener el paciente (evita SQL Injection)
        paciente = Paciente.objects.get(id=id)
    except Paciente.DoesNotExist:
        return Response({
            'mensaje': 'Paciente no encontrado'
        }, status=status.HTTP_404_NOT_FOUND)

    # ✅ SEGURO: Serializador valida y filtra campos
    serializer = PacienteSerializer(paciente, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()  # ✅ Solo guarda campos permitidos

        return Response({
            'mensaje': 'Perfil actualizado exitosamente (método seguro)',
            'datos': serializer.data
        }, status=status.HTTP_200_OK)

    return Response({
        'error': serializer.errors,
        'mensaje': 'Error de validación'
    }, status=status.HTTP_400_BAD_REQUEST)
```

### 🛡️ ¿Cómo el Serializador Previene la Asignación Masiva?

**Archivo**: `servicio_pacientes/pacientes/serializers.py:1-31`

```python
from rest_framework import serializers
from .models import Paciente


class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        # ✅ Solo estos campos están permitidos
        fields = ['id', 'nombre', 'fecha_nacimiento', 'nss', 'email',
                  'password', 'es_doctor', 'fecha_registro', 'fecha_actualizacion']

        extra_kwargs = {
            'password': {'write_only': True},  # ✅ No se expone en respuestas
            'id': {'read_only': True},         # ✅ No se puede modificar
            'fecha_registro': {'read_only': True},     # ✅ No se puede modificar
            'fecha_actualizacion': {'read_only': True}, # ✅ No se puede modificar
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        paciente = Paciente(**validated_data)
        paciente.set_password(password)  # ✅ Password hasheado
        paciente.save()
        return paciente

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)  # ✅ Password hasheado
        instance.save()
        return instance
```

#### Mecanismos de Protección

##### 1. **Lista de Campos Permitidos (`fields`)**

```python
fields = ['id', 'nombre', 'fecha_nacimiento', 'nss', 'email',
          'password', 'es_doctor', 'fecha_registro', 'fecha_actualizacion']
```

- **Solo** los campos en esta lista pueden ser procesados
- Campos no listados son **ignorados automáticamente**
- Proporciona un **whitelist explícito** de campos permitidos

##### 2. **Campos de Solo Lectura (`read_only`)**

```python
extra_kwargs = {
    'id': {'read_only': True},
    'fecha_registro': {'read_only': True'},
    'fecha_actualizacion': {'read_only': True'},
}
```

- **No se pueden modificar** en peticiones PUT/PATCH
- Solo se incluyen en **respuestas GET**
- Django REST Framework los **ignora** si se envían en el request

##### 3. **Campos de Solo Escritura (`write_only`)**

```python
extra_kwargs = {
    'password': {'write_only': True},
}
```

- Se pueden enviar en peticiones POST/PUT
- **No se exponen** en respuestas JSON
- Protege información sensible

##### 4. **Validación Automática**

```python
if serializer.is_valid():
    serializer.save()
```

- **Valida tipos de datos**: `fecha_nacimiento` debe ser una fecha válida
- **Valida formatos**: `email` debe ser un email válido
- **Valida reglas del modelo**: `unique` constraints, `max_length`, etc.
- **Rechaza datos inválidos** antes de tocar la base de datos

##### 5. **Método `update` Controlado**

```python
def update(self, instance, validated_data):
    password = validated_data.pop('password', None)
    for attr, value in validated_data.items():
        setattr(instance, attr, value)  # Solo campos validados
    if password:
        instance.set_password(password)  # Hasheo de password
    instance.save()
    return instance
```

- Solo procesa campos **validados**
- Manejo especial para campos sensibles (password)
- Control granular sobre qué se actualiza

### 🔒 Protección Adicional: Control de Permisos

Para una protección completa contra asignación masiva en el campo `es_doctor`, se puede implementar:

#### Opción 1: Campos Separados por Contexto

```python
class PacienteUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = ['nombre', 'email']  # ❌ es_doctor NO está permitido
        # Solo campos que un usuario normal puede modificar
```

#### Opción 2: Validación Condicional

```python
def update(self, instance, validated_data):
    # Verificar si el usuario intenta cambiar es_doctor
    if 'es_doctor' in validated_data:
        # Verificar permisos del usuario
        if not self.context['request'].user.is_staff:
            raise serializers.ValidationError(
                "No tienes permisos para modificar el rol de doctor"
            )
    # ... resto del código
```

#### Opción 3: Permisos a Nivel de Vista

```python
from rest_framework.permissions import IsAuthenticated, IsAdminUser

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def perfil_seguro(request, id):
    # Solo administradores pueden cambiar es_doctor
    if 'es_doctor' in request.data and not request.user.is_staff:
        return Response({
            'error': 'No autorizado para cambiar rol de doctor'
        }, status=status.HTTP_403_FORBIDDEN)
    # ... resto del código
```

### 📊 Comparación de Resultados

**Ataque: Enviar `{"nombre": "Juan", "es_doctor": true}` a `/perfil/{id}`**

| Endpoint | Comportamiento | Resultado |
|----------|----------------|-----------|
| **Inseguro** | Acepta todos los parámetros | 🔴 `es_doctor` cambia a `true` |
| **Seguro (actual)** | Acepta `es_doctor` pero lo valida | 🟡 `es_doctor` cambia si está en `fields` |
| **Seguro (mejorado)** | Rechaza `es_doctor` para usuarios normales | ✅ `es_doctor` no cambia, error 403 |

### 🔄 Comparación: Inseguro vs. Seguro

| Aspecto | Método Inseguro | Método Seguro |
|---------|-----------------|---------------|
| **Validación de campos** | ❌ Ninguna | ✅ Serializador valida |
| **SQL Injection** | 🔴 Vulnerable | ✅ Protegido por ORM |
| **Asignación Masiva** | 🔴 Vulnerable | ✅ Campos controlados |
| **Campos protegidos** | ❌ Todos modificables | ✅ `read_only` campos |
| **Validación de tipos** | ❌ Ninguna | ✅ Automática |
| **Hasheo de password** | ✅ Implementado | ✅ Implementado |
| **Control de permisos** | ❌ Ninguno | 🟡 Mejorable con permisos |

---

## 3️⃣ Análisis Adicional: Endpoint de Registro

### 🔴 Registro Inseguro (`/inseguro/registro`)

**Archivo**: `servicio_pacientes/pacientes/views.py:10-46`

```python
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

        # 🔴 VULNERABILIDAD: SQL Injection
        query = f"""
            INSERT INTO pacientes_paciente
            (nombre, fecha_nacimiento, nss, email, password, es_doctor, fecha_registro, fecha_actualizacion)
            VALUES ('{nombre}', '{fecha_nacimiento}', '{nss}', '{email}',
                    '{hashed_password}', {es_doctor}, datetime('now'), datetime('now'))
        """

        with connection.cursor() as cursor:
            cursor.execute(query)  # 🔴 Sin sanitización

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
```

### ✅ Registro Seguro (`/seguro/registro`)

**Archivo**: `servicio_pacientes/pacientes/views.py:49-64`

```python
@api_view(['POST'])
def registro_seguro(request):
    # ✅ SEGURO: Serializador valida todos los datos
    serializer = PacienteSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()  # ✅ ORM previene SQL Injection

        return Response({
            'mensaje': 'Paciente registrado exitosamente (método seguro)',
            'datos': serializer.data
        }, status=status.HTTP_201_CREATED)

    return Response({
        'error': serializer.errors,
        'mensaje': 'Error de validación'
    }, status=status.HTTP_400_BAD_REQUEST)
```

---

## 📋 Resumen de Endpoints

### Servicio de Pacientes (Puerto 8000)

| Método | Endpoint | Tipo | Vulnerabilidades |
|--------|----------|------|------------------|
| POST | `/api/pacientes/inseguro/registro` | ⚠️ Inseguro | SQL Injection |
| POST | `/api/pacientes/seguro/registro` | ✅ Seguro | Ninguna |
| PUT | `/api/pacientes/inseguro/perfil/{id}` | ⚠️ Inseguro | SQL Injection + Asignación Masiva |
| PUT | `/api/pacientes/seguro/perfil/{id}` | ✅ Seguro | Ninguna |

### Servicio de Expedientes (Puerto 8001)

| Método | Endpoint | Tipo | Vulnerabilidades |
|--------|----------|------|------------------|
| GET | `/api/expedientes/inseguro/buscar?nss={nss}` | ⚠️ Inseguro | SQL Injection |
| GET | `/api/expedientes/seguro/buscar?nss={nss}` | ✅ Seguro | Ninguna |
| POST | `/api/expedientes/inseguro/crear` | ⚠️ Inseguro | SQL Injection |
| POST | `/api/expedientes/seguro/crear` | ✅ Seguro | Ninguna |

---

## 📮 Colección de Postman

El proyecto incluye una colección completa de Postman: `Sistema de Expedientes Médicos - API.postman_collection.json`

### Cómo Importar

1. Abre **Postman**
2. Click en **Import** (esquina superior izquierda)
3. Selecciona el archivo JSON de la colección
4. La colección se importará con todas las carpetas y endpoints

### Variables de Entorno

- `base_url_pacientes`: http://localhost:8000
- `base_url_expedientes`: http://localhost:8001

### Estructura de la Colección

- **Servicio de Pacientes (Puerto 8000)**
  - Endpoints Seguros ✅
  - Endpoints Inseguros ⚠️
  - Ataques que SÍ Funcionan ✅🔴
  - Ataques Bloqueados por SQLite 🚫

- **Servicio de Expedientes (Puerto 8001)**
  - Endpoints Seguros ✅
  - Endpoints Inseguros ⚠️
  - Ataques que SÍ Funcionan ✅🔴
  - Ataques Bloqueados por SQLite 🚫

---

## 🎯 Conclusiones

### Importancia de las Capas de Abstracción y Validación

Este proyecto demuestra de manera práctica cómo las **capas de abstracción y validación** son fundamentales para la seguridad de aplicaciones web modernas. Los principales aprendizajes son:

#### 1. **Los ORMs son una Capa de Seguridad Crítica**

El uso del **ORM de Django** no es solo una cuestión de conveniencia o productividad, sino una **barrera de seguridad esencial** contra ataques de SQL Injection:

- **Sanitización automática**: Los ORMs escapan y parametrizan automáticamente todas las queries, eliminando la posibilidad de inyección de código SQL.
- **Abstracción del SQL**: Al eliminar la necesidad de escribir SQL manualmente, se reduce drásticamente la superficie de ataque.
- **Validación de tipos**: Los modelos del ORM validan tipos de datos antes de interactuar con la base de datos.

**Lección clave**: Nunca usar SQL raw con concatenación de strings. Si es absolutamente necesario usar SQL directo, siempre usar **parámetros parametrizados** (`cursor.execute(query, [params])`).

#### 2. **Los Serializadores son Guardianes de Datos**

Los **serializadores de Django REST Framework** actúan como una capa de validación robusta que protege contra múltiples tipos de ataques:

- **Whitelist de campos**: Solo los campos explícitamente definidos pueden ser procesados, previniendo asignación masiva.
- **Campos de solo lectura**: Campos críticos como `id`, `fecha_registro`, o metadatos no pueden ser modificados por usuarios.
- **Validación automática**: Tipos de datos, formatos, constraints y reglas de negocio se validan antes de tocar la base de datos.
- **Separación de contextos**: Se pueden crear serializadores diferentes para contextos distintos (creación, actualización, lectura).

**Lección clave**: Nunca confiar en los datos del usuario. Siempre validar, sanitizar y filtrar todos los inputs antes de procesarlos.

#### 3. **Defensa en Profundidad (Defense in Depth)**

La seguridad efectiva no depende de una sola medida, sino de **múltiples capas de protección**:

| Capa | Mecanismo de Protección |
|------|-------------------------|
| **Validación de Input** | Serializadores, validadores personalizados |
| **Capa de Abstracción** | ORM (Django ORM) |
| **Sanitización** | Parámetros parametrizados, escapado automático |
| **Autenticación** | Django Authentication System |
| **Autorización** | Permisos de Django REST Framework |
| **Auditoría** | Campos `fecha_creacion`, `fecha_actualizacion` |
| **Configuración Segura** | `DEBUG=False`, `SECRET_KEY` seguro, HTTPS |

**Lección clave**: Si una capa falla, otras capas deben estar en su lugar para mitigar el daño. Nunca depender de una sola medida de seguridad.

#### 4. **El Costo de la Comodidad**

El código inseguro (SQL raw, sin validación) puede parecer **más directo y simple** a corto plazo, pero:

- **Costo de seguridad**: Expone la aplicación a vulnerabilidades críticas (OWASP Top 10).
- **Costo de mantenimiento**: Código más difícil de mantener y evolucionar.
- **Costo de auditoría**: Difícil de auditar y encontrar vulnerabilidades.
- **Costo de negocio**: Potencial pérdida de datos, multas, daño reputacional.

Por el contrario, el código seguro con ORMs y serializadores:

- **Inversión inicial**: Requiere aprender las herramientas y frameworks.
- **Retorno a largo plazo**: Código más seguro, mantenible, escalable y profesional.
- **Protección automática**: El framework maneja muchas vulnerabilidades automáticamente.

**Lección clave**: La seguridad debe ser una consideración desde el diseño inicial, no un agregado posterior.

#### 5. **SQLite vs. Bases de Datos de Producción**

Es importante destacar que **SQLite tiene limitaciones** que bloquean ciertos ataques (como `DROP TABLE` con `;`):

- SQLite no permite **múltiples sentencias** en `cursor.execute()` por diseño.
- En **MySQL** o **PostgreSQL**, los ataques bloqueados en este proyecto **SÍ funcionarían** en el código inseguro.
- Esto refuerza la importancia de escribir código seguro independientemente de la base de datos utilizada.

**Lección clave**: No confiar en las limitaciones de la tecnología específica. El código debe ser seguro por diseño, no por casualidad.

#### 6. **Educación y Conciencia de Seguridad**

El propósito educativo de este proyecto demuestra que:

- **Entender las vulnerabilidades** es el primer paso para prevenirlas.
- **Ver ataques en acción** ayuda a comprender su impacto real.
- **Comparar código seguro vs. inseguro** ilustra claramente las mejores prácticas.
- **La seguridad es responsabilidad de todos** los desarrolladores, no solo del equipo de seguridad.

**Lección clave**: Invertir en educación de seguridad para todo el equipo de desarrollo es fundamental para construir aplicaciones seguras.

### Recomendaciones para Proyectos Reales

1. **Nunca usar SQL raw con concatenación de strings**
   - Siempre usar el ORM o parámetros parametrizados

2. **Implementar serializadores para todas las APIs**
   - Definir explícitamente qué campos son permitidos, de solo lectura, o de solo escritura

3. **Validar y sanitizar todos los inputs**
   - Nunca confiar en los datos del usuario

4. **Implementar autenticación y autorización robustas**
   - Verificar permisos antes de cualquier operación sensible

5. **Realizar auditorías de seguridad regulares**
   - Pruebas de penetración, revisiones de código, análisis estático

6. **Mantener dependencias actualizadas**
   - Frameworks, librerías y el sistema operativo deben estar al día

7. **Configurar el entorno de producción correctamente**
   - `DEBUG=False`, `SECRET_KEY` seguro, HTTPS, CORS configurado

8. **Implementar logging y monitoreo**
   - Detectar y responder a intentos de ataque

### Reflexión Final

Las vulnerabilidades de seguridad como **SQL Injection** y **Asignación Masiva** siguen estando en el **OWASP Top 10** porque los desarrolladores continúan cometiendo los mismos errores básicos. Este proyecto demuestra que:

- Las herramientas y frameworks modernos (Django, Django REST Framework) **ya proporcionan las soluciones** para estas vulnerabilidades.
- La seguridad no es un problema de falta de herramientas, sino de **educación, conciencia y disciplina** en su uso correcto.
- Escribir código seguro **no es más difícil** que escribir código inseguro cuando se utilizan las abstracciones correctas.

**La seguridad debe ser un requisito fundamental, no opcional, en cualquier proyecto de software.**

---

## 🛠️ Tecnologías Utilizadas

- **Python** 3.13.5
- **Django** 5.2.7
- **Django REST Framework** 3.15.2
- **SQLite3** (base de datos de desarrollo)
- **Git** (control de versiones)

---

## 📁 Estructura del Proyecto

```
ExpedientesMedicos/
│
├── README.md                          # Este archivo
├── .git/                              # Control de versiones
│
├── servicio_pacientes/                # Microservicio 1
│   ├── manage.py
│   ├── requirements.txt
│   ├── db.sqlite3
│   ├── servicio_pacientes/            # Configuración del proyecto
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── ...
│   └── pacientes/                     # App de pacientes
│       ├── models.py                  # Modelo Paciente
│       ├── views.py                   # 4 endpoints (2 seguros, 2 inseguros)
│       ├── serializers.py             # Serializador con validaciones
│       ├── urls.py
│       └── ...
│
└── servicio_expedientes/              # Microservicio 2
    ├── manage.py
    ├── requirements.txt
    ├── db.sqlite3
    ├── servicio_expedientes/          # Configuración del proyecto
    │   ├── settings.py
    │   ├── urls.py
    │   └── ...
    └── expedientes/                   # App de expedientes
        ├── models.py                  # Modelo NotaMedica
        ├── views.py                   # 4 endpoints (2 seguros, 2 inseguros)
        ├── serializers.py             # Serializador con validaciones
        ├── urls.py
        └── ...
```

---

## ⚠️ Advertencia Legal

Este proyecto tiene **fines estrictamente educativos**. Los endpoints inseguros están claramente marcados y **nunca deben usarse en producción**. El uso de técnicas de explotación de vulnerabilidades sin autorización explícita es **ilegal**.

**Uso responsable**:
- ✅ Aprender sobre vulnerabilidades de seguridad
- ✅ Entender cómo proteger aplicaciones
- ✅ Practicar en entornos controlados (localhost)
- ❌ Atacar sistemas sin autorización
- ❌ Usar en producción
- ❌ Compartir técnicas de ataque con fines maliciosos

---

## 📞 Soporte

Para reportar problemas o hacer preguntas sobre el proyecto:
- **Repositorio**: https://github.com/PaulinaCM7/ExpedientesMedicos
- **Issues**: https://github.com/PaulinaCM7/ExpedientesMedicos/issues

---

## 📄 Licencia

Este proyecto es de código abierto y está disponible con fines educativos.

---

**Desarrollado con propósito educativo | Django REST Framework | 2025**
