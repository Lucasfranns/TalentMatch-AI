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

### Herramientas
- Git y GitHub
- Pytest
- Swagger / OpenAPI
- Visual Studio Code

## Funcionalidades implementadas

- API REST desarrollada con FastAPI.
- Registro de ofertas laborales.
- Consulta de todas las ofertas registradas.
- Consulta de una oferta por identificador.
- Validación de datos de entrada mediante Pydantic.
- Persistencia de información en PostgreSQL.
- Gestión de conexiones mediante SQLAlchemy.
- Configuración de credenciales mediante variables de entorno.
- Pruebas automatizadas de endpoints.

## Próximos objetivos

- Implementar gestión completa de ofertas laborales.
- Incorporar carga y procesamiento de currículums.
- Integrar un modelo de Inteligencia Artificial para analizar CV y ofertas.
- Generar informes de compatibilidad entre candidatos y puestos.
- Desarrollar una interfaz web con Next.js y TypeScript.
- Mejorar la cobertura de pruebas y documentación.

## Ejecución local

Desde la raíz del proyecto:

```powershell
backend\.venv\Scripts\Activate.ps1
```

Instalar dependencias:

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

```powershell
python -m pytest backend\tests -v
```

## Estado

En desarrollo.
