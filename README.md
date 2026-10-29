# TalentMatch AI

Aplicación web de análisis asistido por inteligencia artificial que compara los requisitos de una oferta laboral con la evidencia presente en un CV.

## Objetivo

Ayudar a comprender qué requisitos están respaldados por la información del CV, cuáles cuentan con evidencia parcial y cuáles no tienen evidencia identificada.

La herramienta funciona como apoyo para la revisión humana y no toma decisiones automáticas de contratación o rechazo.

## Tecnologías previstas

- **Frontend:** Next.js y TypeScript
- **Backend:** Python y FastAPI
- **Base de datos:** PostgreSQL
- **Inteligencia artificial:** API de un modelo de lenguaje
- **Control de versiones:** Git y GitHub

## Estado

En desarrollo.

### Funcionalidades implementadas

- API REST con FastAPI.
- Creación, listado y consulta de ofertas laborales.
- Validación de datos con Pydantic.
- Pruebas automatizadas con pytest.
- Endpoint de salud para verificar el estado de la API.

### Próximos objetivos

- Persistencia de datos con PostgreSQL.
- Carga y extracción de texto de CV en PDF.
- Análisis asistido por inteligencia artificial.
- Interfaz web con Next.js y TypeScript.

## Aviso de privacidad

La aplicación deberá tratar los CV como información personal, proteger los datos y evitar publicar documentos o credenciales sensibles.
