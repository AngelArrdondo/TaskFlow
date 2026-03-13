# TaskFlow API 🗂️
> Sistema de Gestión de Tareas Personales — REST API

**Versión:** 1.0  
**Framework:** FastAPI 0.110.0  
**Lenguaje:** Python 3.11  
**Base de datos:** MySQL (XAMPP)

---

## Equipo

| Nombre | Rol |
|--------|-----|
| Kevin Cruz Hernández | Desarrollo CRUD tareas |
| Evaristo Junior Gaona Torres | Desarrollo CRUD etiquetas |
| Ángel Silviano Hernández Arredondo | Diseño modelo y endpoints |

**Universidad Tecnológica de Querétaro — LITIID007**  
**Materia:** Aplicaciones Web Orientadas a Servicios  
**Profesora:** Yara Odeth Sainz García

---

## Requisitos para ejecutar

- Python 3.11 o superior
- XAMPP (MySQL corriendo en puerto 3306)
- pip (gestor de paquetes de Python)
- Git

---

## Instalación de dependencias

```bash
# 1. Clonar el repositorio
git clone https://github.com/AngelArrdondo/TaskFlow.git
cd TaskFlow/taskflow-api

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno virtual
# En Linux/Mac:
source venv/bin/activate
# En Windows:
venv\Scripts\activate

# 4. Instalar dependencias
pip install -r requirements.txt
```

### Dependencias incluidas (`requirements.txt`)

```
fastapi==0.110.0
uvicorn==0.27.1
mysql-connector-python==8.3.0
pydantic==2.6.0
python-dotenv==1.0.0
```

---

## Configuración de base de datos

1. Iniciar XAMPP y activar el servicio MySQL
2. Crear la base de datos ejecutando el archivo `database.sql`:

```sql
CREATE DATABASE taskflow_db;
USE taskflow_db;

CREATE TABLE tareas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    descripcion VARCHAR(300),
    fecha_limite DATE,
    completada BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE etiquetas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tarea_etiqueta (
    tarea_id INT,
    etiqueta_id INT,
    PRIMARY KEY (tarea_id, etiqueta_id),
    FOREIGN KEY (tarea_id) REFERENCES tareas(id) ON DELETE CASCADE,
    FOREIGN KEY (etiqueta_id) REFERENCES etiquetas(id) ON DELETE CASCADE
);
```

3. Crear el archivo `.env` en la raíz del proyecto:

```env
DB_USER=root
DB_PASSWORD=
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=taskflow_db
```

---

## Cómo ejecutar

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

El servidor quedará disponible en: `http://localhost:8000`  
Documentación interactiva (Swagger UI): `http://localhost:8000/docs`

---

## Estructura del proyecto

```
taskflow-api/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── controllers/
│   │   ├── tarea_controller.py
│   │   └── etiqueta_controller.py
│   ├── repositories/
│   │   ├── tarea_repository.py
│   │   └── etiqueta_repository.py
│   ├── services/
│   │   ├── tarea_service.py
│   │   └── etiqueta_service.py
│   └── routers/
│       ├── tareas.py
│       └── etiquetas.py
├── .env
├── requirements.txt
├── database.sql
└── README.md
```

---

## Endpoints disponibles

### Tareas

| Método | Ruta | Descripción | Código |
|--------|------|-------------|--------|
| GET | `/api/v1/tareas` | Listar todas las tareas | 200 |
| POST | `/api/v1/tareas` | Crear nueva tarea | 201 |
| GET | `/api/v1/tareas/{id}` | Obtener tarea por ID | 200, 404 |
| PUT | `/api/v1/tareas/{id}` | Actualizar tarea completa | 200, 400, 404 |
| PATCH | `/api/v1/tareas/{id}/completar` | Marcar tarea como completada | 200, 404 |
| DELETE | `/api/v1/tareas/{id}` | Eliminar tarea | 204, 404 |
| POST | `/api/v1/tareas/{id}/etiquetas` | Asignar etiqueta a tarea | 200, 404, 409 |

### Etiquetas

| Método | Ruta | Descripción | Código |
|--------|------|-------------|--------|
| GET | `/api/v1/etiquetas` | Listar todas las etiquetas | 200 |
| POST | `/api/v1/etiquetas` | Crear nueva etiqueta | 201, 400, 409 |

> Parámetros opcionales para GET /api/v1/tareas: `?page=1&limit=10&completada=false`

---

## Ejemplos de request / response

### POST /api/v1/tareas — Crear tarea

**Request:**
```json
{
  "titulo": "Estudiar FastAPI",
  "descripcion": "Revisar validaciones y middlewares",
  "fecha_limite": "2026-03-20"
}
```

**Response 201:**
```json
{
  "status": "success",
  "timestamp": "2026-03-05T10:30:00Z",
  "message": "Tarea creada correctamente",
  "data": {
    "id": 1,
    "titulo": "Estudiar FastAPI",
    "descripcion": "Revisar validaciones y middlewares",
    "fecha_limite": "2026-03-20",
    "completada": false
  }
}
```

---

### GET /api/v1/tareas — Listar tareas

**Response 200:**
```json
{
  "status": "success",
  "timestamp": "2026-03-05T10:30:00Z",
  "message": "Lista de tareas",
  "data": [
    {
      "id": 1,
      "titulo": "Estudiar FastAPI",
      "descripcion": "Revisar validaciones",
      "fecha_limite": "2026-03-20",
      "completada": false,
      "etiquetas": [{ "id": 1, "nombre": "Urgente" }]
    }
  ],
  "meta": { "page": 1, "limit": 10, "total": 1 }
}
```

---

### GET /api/v1/tareas/9999 — ID inexistente

**Response 404:**
```json
{
  "status": "error",
  "timestamp": "2026-03-05T10:30:00Z",
  "message": "Tarea no encontrada",
  "error_code": "TASK_NOT_FOUND"
}
```

---

### POST /api/v1/tareas — Sin título (error de validación)

**Request:**
```json
{
  "descripcion": "Esta tarea no tiene título y debe fallar",
  "fecha_limite": "2026-03-20"
}
```

**Response 400:**
```json
{
  "status": "error",
  "timestamp": "2026-03-05T10:30:00Z",
  "message": "Error de validación",
  "error_code": "VALIDATION_ERROR"
}
```

---

### POST /api/v1/etiquetas — Crear etiqueta

**Request:**
```json
{
  "nombre": "Urgente"
}
```

**Response 201:**
```json
{
  "status": "success",
  "timestamp": "2026-03-05T10:30:00Z",
  "message": "Etiqueta creada correctamente",
  "data": { "id": 1, "nombre": "Urgente" }
}
```

---

### PATCH /api/v1/tareas/{id}/completar — Marcar como completada

**Response 200:**
```json
{
  "status": "success",
  "timestamp": "2026-03-05T10:30:00Z",
  "message": "Tarea actualizada correctamente",
  "data": {
    "id": 1,
    "titulo": "Estudiar FastAPI",
    "completada": true
  }
}
```

---

## Evidencia de pruebas

- 📹 **Video demostración** (servidor, Postman y Swagger):  
  https://drive.google.com/drive/folders/1TliMZm0xHtL4B8NKrH3zcbXI4DxKWRNC?usp=drive_link

- 💻 **Repositorio GitHub**:  
  https://github.com/AngelArrdondo/TaskFlow.git

- 📄 **Documentación Swagger (local)**:  
  http://localhost:8000/docs

### Pruebas realizadas

| ID | Caso | Resultado |
|----|------|-----------|
| CP01 | Crear tarea válida | ✅ 201 Created |
| CP02 | Listar tareas con paginación | ✅ 200 OK |
| CP03 | Actualizar tarea (PUT) | ✅ 200 OK |
| CP04 | Cambio de estado (PATCH) | ✅ 200 OK |
| CP05 | Crear etiqueta | ✅ 201 Created |
| CP06 | Asignar etiqueta a tarea | ✅ 200 OK |
| CP07 | Eliminar tarea | ✅ 204 No Content |
| CP08 | Datos incompletos (sin título) | ✅ 400 Bad Request |
| CP09 | ID inexistente | ✅ 404 Not Found |

---

*TaskFlow API v1.0 — Universidad Tecnológica de Querétaro, 2026*