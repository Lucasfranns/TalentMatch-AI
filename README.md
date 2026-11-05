# TalentMatch AI

**Sistema de análisis asistido de CV y ofertas laborales mediante Inteligencia Artificial.**

Proyecto en desarrollo como iniciativa de aprendizaje y portfolio profesional.

## Descripción

TalentMatch AI busca facilitar el proceso de postulación laboral mediante el análisis de ofertas de trabajo y currículums, identificando coincidencias entre los requisitos solicitados y las competencias de los candidatos.

El objetivo es proporcionar información útil para la toma de decisiones, sin reemplazar el criterio humano en los procesos de selección.

## Tecnologías

### Backend
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic

### Testing
- Pytest
- HTTPX

### Herramientas
- Git y GitHub
- Swagger / OpenAPI
- Visual Studio Code

## Funcionalidades implementadas

- API REST desarrollada con FastAPI.
- Registro de ofertas laborales.
- Consulta de todas las ofertas registradas.
- Consulta de una oferta por identificador.
- Actualización de ofertas existentes.
- Eliminación de ofertas.
- Validación de datos de entrada mediante Pydantic.
- Persistencia de información en PostgreSQL.
- Gestión de conexiones mediante SQLAlchemy.
- Configuración de credenciales mediante variables de entorno.
- Pruebas automatizadas de endpoints con Pytest.

## Próximos objetivos

- Incorporar carga de currículums en formato PDF.
- Extraer y procesar el texto de los currículums.
- Almacenar la información de los candidatos en PostgreSQL.
- Integrar un modelo de Inteligencia Artificial para analizar CV y ofertas.
- Generar informes de compatibilidad entre candidatos y puestos.
- Desarrollar una interfaz web con Next.js y TypeScript.
- Mejorar la cobertura de pruebas y documentación.

## Ejecución local

Desde la raíz del proyecto, activar el entorno virtual:

```powershell
backend\.venv\Scripts\Activate.ps1
```

Instalar las dependencias:

```powershell
pip install -r backend\requirements.txt
```

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

## Estado

En desarrollo.