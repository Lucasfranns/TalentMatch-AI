# TalentMatch AI

**Sistema de análisis asistido de CV y ofertas laborales mediante Inteligencia Artificial.**

Proyecto en desarrollo como iniciativa de aprendizaje y portfolio profesional.

## Descripción

TalentMatch AI busca facilitar el proceso de postulación laboral mediante el análisis de ofertas de trabajo y currículums, identificando coincidencias entre los requisitos solicitados y las competencias de los candidatos.

El objetivo es proporcionar información útil para la toma de decisiones, sin reemplazar el criterio humano en los procesos de selección.

## Tecnologías

### Backend
- Python 3.12
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic

### Procesamiento de documentos
- pypdf
- python-multipart

### Testing
- Pytest
- HTTPX
- SQLite para pruebas automatizadas

### Herramientas
- Git y GitHub
- Swagger / OpenAPI
- Visual Studio Code

## Funcionalidades implementadas

### Gestión de ofertas laborales
- Registro de ofertas laborales.
- Consulta de todas las ofertas registradas.
- Consulta de una oferta por identificador.
- Actualización de ofertas existentes.
- Eliminación de ofertas.
- Validación de datos de entrada mediante Pydantic.

### Gestión de currículums
- Carga de currículums en formato PDF.
- Validación del formato y tamaño de los archivos (máximo 10 MB).
- Rechazo de archivos inválidos y documentos protegidos con contraseña.
- Extracción de texto mediante pypdf.
- Detección de documentos sin texto extraíble.
- Almacenamiento de archivos PDF en el servidor.
- Persistencia de metadatos y texto extraído en PostgreSQL.
- Consulta de todos los currículums registrados.
- Consulta de un currículum por identificador.
- Eliminación de currículums y sus archivos asociados.

### Infraestructura y calidad
- API REST desarrollada con FastAPI.
- Persistencia mediante PostgreSQL y SQLAlchemy.
- Configuración de credenciales mediante variables de entorno.
- Documentación interactiva mediante Swagger.
- Pruebas automatizadas de endpoints con Pytest.

## Endpoints disponibles

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/health` | Verificar estado de la API |
| POST | `/jobs` | Crear oferta laboral |
| GET | `/jobs` | Listar ofertas |
| GET | `/jobs/{job_id}` | Consultar oferta |
| PUT | `/jobs/{job_id}` | Actualizar oferta |
| DELETE | `/jobs/{job_id}` | Eliminar oferta |
| POST | `/resumes` | Cargar currículum PDF |
| GET | `/resumes` | Listar currículums |
| GET | `/resumes/{resume_id}` | Consultar currículum |
| DELETE | `/resumes/{resume_id}` | Eliminar currículum |

## Ejecución local

Desde la raíz del proyecto, activar el entorno virtual:

```powershell
backend\.venv\Scripts\Activate.ps1
```

Instalar las dependencias:

```powershell
pip install -r backend\requirements.txt
```

Configurar la variable `DATABASE_URL` en un archivo `.env` ubicado en la raíz del proyecto.

Iniciar el servidor:

```powershell
python -m uvicorn backend.main:app --reload
```

La documentación interactiva estará disponible en:

`http://127.0.0.1:8000/docs`

## Pruebas

Ejecutar todas las pruebas automatizadas:

```powershell
python -m pytest backend\tests -v
```

Las pruebas utilizan una base de datos SQLite independiente para evitar modificar los datos de desarrollo en PostgreSQL.

**Estado actual: 17 pruebas aprobadas.**

## Próximos objetivos

- Implementar análisis de compatibilidad entre currículums y ofertas laborales.
- Integrar un modelo de Inteligencia Artificial para interpretar requisitos y competencias.
- Generar informes explicativos de coincidencias y brechas de habilidades.
- Desarrollar una interfaz web con Next.js y TypeScript.
- Mejorar la cobertura de pruebas y documentación.

## Estado

En desarrollo.