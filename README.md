# Sistema de Expedientes Médicos Simplificado (API REST)

## 📖 Descripción del Proyecto

Sistema backend para gestionar expedientes médicos de una clínica mediante una arquitectura de **microservicios**. La API está diseñada para ser consumida por diferentes clientes (aplicación web para doctores, app móvil para pacientes, etc.).

El sistema maneja dos tipos de roles:
- **DOCTOR**: Puede crear y consultar notas médicas
- **PACIENTE**: Puede consultar sus propios expedientes médicos

### Propósito Educativo

Este proyecto tiene un **propósito educativo** y demuestra de manera práctica:
- ✅ Vulnerabilidades críticas de seguridad (SQL Injection, Asignación Masiva)
- ✅ Diferencias entre código seguro e inseguro
- ✅ Importancia del uso de ORMs y validadores
- ✅ Arquitectura de microservicios
- ✅ Mejores prácticas en desarrollo de APIs REST
---

## 🏗️ Arquitectura

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
- **Base de datos**: pacientes_paciente
- **Puerto**: 8000

### Microservicio 2: Servicio de Expedientes
- **Responsabilidad**: Gestión de notas médicas y expedientes clínicos
- **Base de datos**: expedientes_notamedica
- **Puerto**: 8001

---

## 💻 Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git
- Postman o Insomnia (opcional, para probar endpoints)
- Virtual environment (recomendado)

---

## 🚀 Instalación

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

---

## ⚙️ Configuración

### Configuración de Puertos

Para ejecutar ambos servicios simultáneamente, deben usar diferentes puertos:

- **Servicio de Pacientes**: Puerto 8000
- **Servicio de Expedientes**: Puerto 8001

---

## ▶️ Ejecución

Necesitas **dos terminales** para ejecutar ambos servicios simultáneamente:

### Terminal 1: Servicio de Pacientes
```bash
cd servicio_pacientes
python manage.py runserver 8000
```

### Terminal 2: Servicio de Expedientes
```bash
cd servicio_expedientes
python manage.py runserver 8001
```

### Verificar que los servicios están funcionando

- Servicio de Pacientes: http://localhost:8000/admin/
- Servicio de Expedientes: http://localhost:8001/admin/

---

## 📚 Documentación de APIs

### 🔹 Servicio de Pacientes (Puerto 8000)

#### Modelo de Datos: Paciente

```json
{
    "id": 1,
    "nombre": "Juan Pérez García",
    "fecha_nacimiento": "1990-05-15",
    "nss": "12345678901",
    "email": "juan.perez@example.com",
    "password": "hasheado_automaticamente",
    "es_doctor": false,
    "fecha_registro": "2025-10-31T10:30:00Z",
    "fecha_actualizacion": "2025-10-31T10:30:00Z"
}
```

#### Endpoints Disponibles

| Método | Endpoint | Tipo | Descripción |
|--------|----------|------|-------------|
| POST | `/api/pacientes/inseguro/registro` | ⚠️ Inseguro | Registro con SQL Injection |
| POST | `/api/pacientes/seguro/registro` | ✅ Seguro | Registro usando ORM |
| PUT | `/api/pacientes/inseguro/perfil/{id}` | ⚠️ Inseguro | Actualización con SQL Injection |
| PUT | `/api/pacientes/seguro/perfil/{id}` | ✅ Seguro | Actualización usando ORM |

---

### 🔹 Servicio de Expedientes (Puerto 8001)

#### Modelo de Datos: NotaMedica

```json
{
    "id": 1,
    "id_paciente": 5,
    "id_doctor": 2,
    "fecha_consulta": "2025-10-31T14:30:00Z",
    "diagnostico": "Gripe estacional con fiebre alta",
    "tratamiento": "Reposo, Paracetamol 500mg cada 8 horas",
    "fecha_creacion": "2025-10-31T14:35:00Z",
    "fecha_actualizacion": "2025-10-31T14:35:00Z"
}
```

#### Endpoints Disponibles

| Método | Endpoint | Tipo | Descripción |
|--------|----------|------|-------------|
| GET | `/api/expedientes/inseguro/buscar?nss={nss}` | ⚠️ Inseguro | Búsqueda con SQL Injection |
| GET | `/api/expedientes/seguro/buscar?nss={nss}` | ✅ Seguro | Búsqueda usando ORM |
| POST | `/api/expedientes/inseguro/crear` | ⚠️ Inseguro | Creación con SQL Injection |
| POST | `/api/expedientes/seguro/crear` | ✅ Seguro | Creación usando ORM |

---

## 🔓 Vulnerabilidades Implementadas

### 1. SQL Injection

**Endpoints afectados** (todos los marcados como "inseguro"):
- POST `/api/pacientes/inseguro/registro`
- PUT `/api/pacientes/inseguro/perfil/{id}`
- GET `/api/expedientes/inseguro/buscar?nss={nss}`
- POST `/api/expedientes/inseguro/crear`

**¿Qué es?**
Los datos del usuario se concatenan directamente en queries SQL sin sanitización.

**Código vulnerable:**
```python
# ⚠️ INSEGURO - NO USAR EN PRODUCCIÓN
nss = request.GET.get('nss')
query = f"SELECT * FROM pacientes_paciente WHERE nss = '{nss}'"
cursor.execute(query)
```

**Código seguro:**
```python
# ✅ SEGURO - Usar ORM
paciente = Paciente.objects.filter(nss=nss).first()
```

### 2. Asignación Masiva

**Endpoints afectados**:
- PUT `/api/pacientes/inseguro/perfil/{id}`

**¿Qué es?**
Permite modificar campos no autorizados enviando parámetros adicionales.

**Ataque de ejemplo:**
```json
PUT /api/pacientes/inseguro/perfil/5
{
    "nombre": "Atacante",
    "es_doctor": true  // ⚠️ Campo que no debería modificarse
}
```

**Mitigación:**
El serializador seguro solo permite modificar campos específicos definidos en `fields`.

---

## 📝 Ejemplos de Uso

### Ejemplo 1: Registrar un Paciente (SEGURO)

```bash
POST http://localhost:8000/api/pacientes/seguro/registro
Content-Type: application/json

{
    "nombre": "María González",
    "fecha_nacimiento": "1985-03-20",
    "nss": "98765432101",
    "email": "maria.gonzalez@example.com",
    "password": "MiPassword123",
    "es_doctor": false
}
```

**Respuesta exitosa:**
```json
{
    "mensaje": "Paciente registrado exitosamente (método seguro)",
    "datos": {
        "id": 1,
        "nombre": "María González",
        "fecha_nacimiento": "1985-03-20",
        "nss": "98765432101",
        "email": "maria.gonzalez@example.com",
        "es_doctor": false,
        "fecha_registro": "2025-10-31T10:30:00Z",
        "fecha_actualizacion": "2025-10-31T10:30:00Z"
    }
}
```

---

### Ejemplo 2: Registrar un Doctor (SEGURO)

```bash
POST http://localhost:8000/api/pacientes/seguro/registro
Content-Type: application/json

{
    "nombre": "Dr. Carlos Ramírez",
    "fecha_nacimiento": "1975-08-15",
    "nss": "11223344556",
    "email": "carlos.ramirez@clinica.com",
    "password": "DocPassword456",
    "es_doctor": true
}
```

---

### Ejemplo 3: Crear Nota Médica (SEGURO)

```bash
POST http://localhost:8001/api/expedientes/seguro/crear
Content-Type: application/json

{
    "id_paciente": 1,
    "id_doctor": 2,
    "fecha_consulta": "2025-10-31T14:30:00",
    "diagnostico": "Gripe estacional con fiebre de 38.5°C, dolor de garganta y congestión nasal",
    "tratamiento": "Reposo absoluto por 3 días. Paracetamol 500mg cada 8 horas. Abundantes líquidos"
}
```

**Respuesta exitosa:**
```json
{
    "mensaje": "Nota médica creada exitosamente (método seguro)",
    "datos": {
        "id": 1,
        "id_paciente": 1,
        "id_doctor": 2,
        "fecha_consulta": "2025-10-31T14:30:00Z",
        "diagnostico": "Gripe estacional con fiebre de 38.5°C...",
        "tratamiento": "Reposo absoluto por 3 días...",
        "fecha_creacion": "2025-10-31T14:35:00Z",
        "fecha_actualizacion": "2025-10-31T14:35:00Z"
    }
}
```

---

### Ejemplo 4: Buscar Expedientes por NSS (SEGURO)

```bash
GET http://localhost:8001/api/expedientes/seguro/buscar?nss=98765432101
```

**Respuesta exitosa:**
```json
{
    "mensaje": "Notas médicas encontradas (método seguro)",
    "total": 3,
    "notas": [
        {
            "id": 3,
            "id_paciente": 1,
            "id_doctor": 2,
            "fecha_consulta": "2025-10-31T14:30:00Z",
            "diagnostico": "Control médico rutinario",
            "tratamiento": "Ninguno. Paciente en buen estado de salud",
            "fecha_creacion": "2025-10-31T14:35:00Z",
            "fecha_actualizacion": "2025-10-31T14:35:00Z"
        }
    ]
}
```

---

### Ejemplo 5: Actualizar Perfil (SEGURO)

```bash
PUT http://localhost:8000/api/pacientes/seguro/perfil/1
Content-Type: application/json

{
    "nombre": "María González López",
    "email": "maria.gonzalez.nuevo@example.com"
}
```

---

### ⚠️ Ejemplos de ATAQUES (Fines Educativos)

#### Ataque 1: SQL Injection en Búsqueda

```bash
# Intento de obtener TODOS los registros
GET http://localhost:8001/api/expedientes/inseguro/buscar?nss=123' OR '1'='1

# Intento de eliminar tabla
GET http://localhost:8001/api/expedientes/inseguro/buscar?nss=123'; DROP TABLE expedientes_notamedica; --
```

#### Ataque 2: SQL Injection en Registro

```bash
POST http://localhost:8000/api/pacientes/inseguro/registro
Content-Type: application/json

{
    "nombre": "Test'; DROP TABLE pacientes_paciente; --",
    "fecha_nacimiento": "1990-01-01",
    "nss": "12345678901",
    "email": "test@test.com",
    "password": "test123",
    "es_doctor": false
}
```

#### Ataque 3: Asignación Masiva

```bash
# Intentar convertirse en doctor sin autorización
PUT http://localhost:8000/api/pacientes/inseguro/perfil/1
Content-Type: application/json

{
    "nombre": "Atacante",
    "es_doctor": true  // ⚠️ Campo no autorizado
}
```

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
│   ├── .gitignore
│   │
│   ├── servicio_pacientes/            # Configuración del proyecto
│   │   ├── __init__.py
│   │   ├── settings.py                # Configuración Django
│   │   ├── urls.py                    # URLs principales
│   │   ├── wsgi.py
│   │   └── asgi.py
│   │
│   └── pacientes/                     # App de pacientes
│       ├── __init__.py
│       ├── models.py                  # Modelo Paciente
│       ├── views.py                   # 4 endpoints (2 seguros, 2 inseguros)
│       ├── serializers.py             # Serializador con validaciones
│       ├── urls.py                    # Rutas de la app
│       ├── admin.py                   # Configuración del admin
│       ├── apps.py
│       ├── tests.py
│       └── migrations/
│           └── 0001_initial.py
│
└── servicio_expedientes/              # Microservicio 2
    ├── manage.py
    ├── requirements.txt
    ├── db.sqlite3
    ├── .gitignore
    │
    ├── servicio_expedientes/          # Configuración del proyecto
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── urls.py
    │   ├── wsgi.py
    │   └── asgi.py
    │
    └── expedientes/                   # App de expedientes
        ├── __init__.py
        ├── models.py                  # Modelo NotaMedica
        ├── views.py                   # 4 endpoints (2 seguros, 2 inseguros)
        ├── serializers.py             # Serializador con validaciones
        ├── urls.py                    # Rutas de la app
        ├── admin.py                   # Configuración del admin
        ├── apps.py
        ├── tests.py
        └── migrations/
            └── 0001_initial.py
```

---

## 🛠️ Tecnologías Utilizadas

- **Python** 3.13.5
- **Django REST Framework** 3.15.2 - Framework para APIs REST
- **SQLite3** - Base de datos (desarrollo)
- **Git** - Control de versiones

### Dependencias (requirements.txt)

```
Django==5.2.7
djangorestframework==3.15.2
```

### ✅ Mejores Prácticas Implementadas

- Hasheo de contraseñas con algoritmos seguros
- Validación de datos con serializers
- Uso de ORM para prevenir SQL Injection
- Campos read-only para metadatos
- Validadores personalizados

---

## 📊 Diagramas

### Flujo de Registro de Paciente (Seguro)

```
Cliente → POST /api/pacientes/seguro/registro
         ↓
    Serializador valida datos
         ↓
    Password es hasheado
         ↓
    ORM crea registro (previene SQL Injection)
         ↓
    Respuesta JSON con datos (sin password)
```

### Flujo de Búsqueda de Expedientes (Seguro)

```
Cliente → GET /api/expedientes/seguro/buscar?nss=XXX
         ↓
    Validar parámetro NSS
         ↓
    ORM busca paciente por NSS (sanitizado)
         ↓
    ORM busca notas del paciente
         ↓
    Serializar notas médicas
         ↓
    Respuesta JSON con lista de notas
```