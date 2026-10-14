# WORSHIP Mascot Robot — Backend

## Visión General

Este microservicio backend proporciona los componentes faciales iniciales necesarios para renderizar el rostro de la mascota robótica WORSHIP mediante un endpoint REST.

## 1. Endpoint de Rostro Inicial

### 1.1 Objetivo
Proporcionar los componentes faciales iniciales necesarios para renderizar el rostro de la mascota robótica. Estos componentes se obtienen de la carpeta `emociones` y se envían en formato JSON con datos codificados en Base64.

### 1.2 Componentes Faciales
Los siguientes archivos representan los componentes faciales básicos:
- `emociones/boca/boca.png` - Boca
- `emociones/nariz/nariz.png` - Nariz  
- `emociones/ojo-derecho/ojo-derecho.png` - Ojo derecho
- `emociones/ojo-izquierdo/ojo-izquierdo.png` - Ojo izquierdo

### 1.3 Endpoint
```
GET /api/v1/face/initial
```

### 1.4 Respuesta Ejemplo
```json
{
  "success": true,
  "components": [
    {
      "name": "boca",
      "type": "image/png",
      "data": "BASE64_IMAGE_DATA"
    },
    {
      "name": "nariz", 
      "type": "image/png",
      "data": "BASE64_IMAGE_DATA"
    },
    {
      "name": "ojo-derecho",
      "type": "image/png", 
      "data": "BASE64_IMAGE_DATA"
    },
    {
      "name": "ojo-izquierdo",
      "type": "image/png",
      "data": "BASE64_IMAGE_DATA"
    }
  ]
}
```

## 2. Tecnologías

- **Python:** lenguaje principal
- **FastAPI:** API REST
- **Pydantic:** validación de solicitudes y respuestas
- **Uvicorn:** servidor de desarrollo

## 3. Arquitectura MVC

Se utiliza MVC adaptado a una API REST:

- **Models:** esquemas Pydantic para validar datos (`app/models/face_component.py`)
- **Views:** representación de respuestas HTTP en JSON (`app/views/face_view.py`)
- **Controllers:** recepción y coordinación de solicitudes (`app/controllers/face_controller.py`)
- **Services:** lectura, procesamiento y codificación de imágenes (`app/services/face_service.py`)
- **Repositories:** consulta del catálogo de componentes y acceso a los archivos (`app/repositories/face_repository.py`)
- **Main:** inicialización de FastAPI y registro de rutas (`app/main.py`)

## 4. Estructura del Backend

```text
backend/
├── app/
│   ├── main.py
│   │
│   ├── controllers/
│   │   └── face_controller.py
│   │
│   ├── models/
│   │   └── face_component.py
│   │
│   ├── views/
│   │   └── face_view.py
│   │
│   ├── services/
│   │   └── face_service.py
│   │
│   ├── repositories/
│   │   └── face_repository.py
│   │
│   └── assets/
│       └── emociones/
│           ├── boca/
│           │   └── boca.png
│           ├── nariz/
│           │   └── nariz.png
│           ├── ojo-derecho/
│           │   └── ojo-derecho.png
│           └── ojo-izquierdo/
│               └── ojo-izquierdo.png
├── tests/
│   └── test_face_initial.py
├── docs/
│   ├── 01-arquitectura.md
│   ├── 02-diagrama-clases.md
│   ├── 03-casos-de-uso.md
│   ├── 04-flujo-endpoint.md
│   └── 05-flujo-usuario.md
├── requirements.txt
├── .env.example
└── README.md
```

## 5. Funcionamiento del Servicio

```text
Usuario
    |
    | GET /api/v1/face/initial
    v
FastAPI — Router
    |
    v
FaceController
    |
    v
FaceService
    |
    v
FaceRepository
    |
    v
Sistema de archivos (emociones/)
    |
    v
FaceRepository (codifica a Base64)
    |
    v
FaceService
    |
    v
FaceController
    |
    v
FaceView (formatea respuesta JSON)
    |
    v
FastAPI — Response
    |
    v
Frontend Astro + React
```

## 6. Instalación y Ejecución

1. Crear entorno virtual: `python -m venv .venv`
2. Activar el entorno virtual:
   - Windows: `.venv\Scripts\activate`
   - Linux/macOS: `source .venv/bin/activate`
3. Instalar dependencias: `pip install -r requirements.txt`
4. Iniciar el servidor: `uvicorn app.main:app --reload`
5. La documentación interactiva estará disponible en:
    - `http://127.0.0.1:8000/docs`
    - `http://127.0.0.1:8000/redoc`
6. Probar el endpoint: `http://127.0.0.1:8000/api/v1/face/initial`
   - Debería retornar un JSON con `success: true` y una lista de 4 componentes faciales codificados en Base64.

## 7. Seguridad y Validaciones

- Validar existencia de todos los archivos PNG configurados
- Verificar que los archivos puedan leerse correctamente
- Validar la estructura de salida mediante Pydantic
- Gestionar errores de lectura y archivos inexistentes con HTTP apropiados
- Mantener una lista centralizada de componentes en el repositorio
- No revelar rutas internas ni trazas en los mensajes de error

## 8. Próximos Pasos

- [ ] Implementar pruebas automatizadas completas
- [ ] Añadir documentación detallada en los archivos de docs/
- [ ] Preparar integración con frontend Astro + React
- [ ] Diseñar estructura para futuros endpoints (parpadeo, emociones, etc.)