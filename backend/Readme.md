# WORSHIP Mascot Robot — Backend

## Visión General

Este microservicio backend gestiona las expresiones faciales y parpadeos de la mascota robótica WORSHIP mediante dos endpoints principales:
1. **Endpoint de rostro inicial**: Envía los componentes faciales básicos (ojos, nariz, boca) en formato JSON
2. **Endpoint de parpadeo**: Activa la animación de parpadeo cambiando las imágenes de los ojos

## 1. Endpoint de Rostro Inicial

### 1.1 Objetivo
Proporcionar los componentes faciales iniciales necesarios para renderizar el rostro de la mascota robótica. Estos componentes se obtienen de la carpeta `emociones` y se envían en grupos de 5 elementos a través de un endpoint REST.

### 1.2 Componentes Faciales
Los siguientes archivos representan los componentes faciales básicos:
- `emociones/boca/boca.png` - Boca
- `emociones/nariz/nariz.png` - Nariz  
- `emociones/ojo-derecho/ojo-derecho.png` - Ojo derecho
- `emociones/ojo-izquierdo/ojo-izquierdo.png` - Ojo izquierdo
- *(Componente adicional para completar el grupo de 5 - por definir)*

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
      "data": "base64_encoded_string"
    },
    {
      "name": "nariz", 
      "type": "image/png",
      "data": "base64_encoded_string"
    },
    {
      "name": "ojo-derecho",
      "type": "image/png", 
      "data": "base64_encoded_string"
    },
    {
      "name": "ojo-izquierdo",
      "type": "image/png",
      "data": "base64_encoded_string"
    }
    // Quinto componente por definir
  ]
}
```

## 2. Endpoint de Parpadeo

### 2.1 Objetivo
Interpretar instrucciones de texto mediante Groq y convertirlas en acciones de parpadeo estructuradas para la mascota robótica.

### 2.2 Tecnologías
- **Python:** lenguaje principal
- **FastAPI:** API REST
- **Groq:** inferencia del modelo de IA
- **Pydantic:** validación de solicitudes y respuestas
- **Uvicorn:** servidor de desarrollo
- **python-dotenv:** gestión de variables de entorno

### 2.3 Funcionamiento del Servicio
```text
Usuario
    |
    | POST /api/v1/robot/interpret
    | JSON: {"text": "Parpadea dos veces"}
    v
FastAPI — Controller
    |
    v
GroqService
    |
    | Interpreta intención y cantidad
    v
Modelo de IA Groq
    |
    | Respuesta estructurada
    v
Controller + validación
    |
    v
AnimationService
    |
    | Selecciona recurso disponible
    v
Respuesta JSON
    |
    v
Frontend Astro + React
```

### 2.4 Arquitectura MVC
Se utiliza MVC adaptado a una API REST:

- **Models:** esquemas Pydantic para validar datos
- **Views:** representación de respuestas HTTP en JSON
- **Controllers:** recepción y coordinación de solicitudes
- **Services:** integración con Groq y selección de animaciones
- **Repositories:** consulta del catálogo de animaciones
- **animations/:** recursos visuales locales de parpadeo

### 2.5 Estructura del Backend
```text
backend/
├── app/
│   ├── main.py
│   │
│   ├── controllers/
│   │   └── robot_controller.py
│   │
│   ├── models/
│   │   ├── robot_request.py
│   │   ├── robot_response.py
│   │   └── groq_interpretation.py
│   │
│   ├── views/
│   │   └── robot_view.py
│   │
│   ├── services/
│   │   ├── groq_service.py
│   │   └── animation_service.py
│   │
│   ├── repositories/
│   │   └── animation_repository.py
│   │
│   └── animations/
│       └── blink/
│           ├── variant_01/
│           │   ├── frame_01
│           │   ├── frame_02
│           │   └── frame_03
│           │
│           ├── variant_02/
│           │   ├── frame_01
│           │   ├── frame_02
│           │   └── frame_03
│           │
│           └── variant_03/
│               ├── frame_01
│               ├── frame_02
│               └── frame_03
│
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

### 2.6 API de Parpadeo
#### POST /api/v1/robot/interpret
Recibe texto y devuelve la interpretación junto con la acción de parpadeo y referencia visual.

**Solicitud:**
```json
{
  "text": "Parpadea dos veces"
}
```

**Respuesta de ejemplo:**
```json
{
  "success": true,
  "intent": "blink",
  "should_blink": true,
  "count": 2,
  "animation": {
    "variant": "variant_02",
    "frames": [
      "frame_01",
      "frame_02", 
      "frame_03"
    ]
  }
}
```

### 2.7 Integración con Groq
Groq interpreta el texto del usuario para identificar:
- `intent`: debe ser "blink" para activar parpadeo
- `should_blink`: boolean que indica si se debe parpadear
- `count`: número entero de parpadeos solicitados

La clave de Groq se almacena en variable de entorno:
```env
GROQ_API_KEY=tu_clave_de_groq
```

### 2.8 Instalación y Ejecución
1. Crear entorno virtual: `python -m venv .venv`
2. Activar (Windows): `.venv\Scripts\activate`
3. Instalar dependencias: `pip install -r requirements.txt`
4. Configurar `.env` con `GROQ_API_KEY`
5. Iniciar: `uvicorn app.main:app --reload`
6. Documentación: `http://127.0.0.1:8000/docs`

## 3. Seguridad y Validaciones
- Mantener clave de Groq fuera del código fuente
- Validar entradas con Pydantic
- Limitar cantidad máxima de parpadeos
- Verificar existencia de variantes y recursos
- Manejar errores de red e inferencia controladamente
- Prevenir inyección de comandos mediante IA
- Añadir pruebas para casos edge

## 4. Próximos Pasos
- [ ] Implementar endpoint de rostro inicial
- [ ] Implementar endpoint de parpadeo
- [ ] Definir quinto componente facial
- [ ] Crear catálogo de animaciones de parpadeo
- [ ] Integrar con frontend Astro + React