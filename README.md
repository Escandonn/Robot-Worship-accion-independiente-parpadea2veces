# WORSHIP Mascot Robot

## Visión General del Proyecto

Plataforma de interacción que combina representación visual animada, lógica de comportamiento y arquitectura backend preparada para IA y control de componentes físicos.

## Arquitectura del Sistema

### 1. Frontend (Astro + React)
- **Responsabilidad:** Interfaz y representación visual de la mascota
- **Funciones:**
  - Mostrar rostro y ojos del robot
  - Ejecutar animaciones y transiciones
  - Gestionar estados visuales (reposo, parpadeo, expresiones)
  - Recibir instrucciones del backend
  - Separar lógica visual de toma de decisiones

### 2. Backend (Python + FastAPI)
- **Responsabilidad:** Coordinar acciones y comunicar módulos del sistema
- **Funciones:**
  - Exponer API para recibir instrucciones
  - Validar acciones solicitadas
  - Coordinar módulo de comportamiento
  - Integrar modelo de IA cuando corresponda
  - Entregar instrucciones estructuradas al frontend
  - Preparar integración futura con MQTT y dispositivos físicos

### 3. Componentes Visuales (emociones/)
- **Responsabilidad:** Almacenar assets faciales básicos
- **Contenido:**
  - `boca/boca.png` - Componente de boca
  - `nariz/nariz.png` - Componente de nariz
  - `ojo-derecho/ojo-derecho.png` - Componente de ojo derecho
  - `ojo-izquierdo/ojo-izquierdo.png` - Componente de ojo izquierdo
  - *[Quinto componente por definir]*

## Endpoints Principales

### 1. Endpoint de Rostro Inicial
**Propósito:** Proporcionar componentes faciales básicos para renderizado inicial
**Endpoint:** `GET /api/v1/face/initial`
**Funcionalidad:**
- Lee componentes de la carpeta `emociones/`
- Los envía en formato JSON como imágenes base64
- Proporciona el estado visual base del robot

### 2. Endpoint de Interpretación de Texto
**Propósito:** Interpretar instrucciones de texto mediante IA y generar respuestas estructuradas (texto, imagen o animación)
**Endpoint:** `POST /api/v1/robot/interpret`
**Tecnologías:** Python, FastAPI, Groq, Pydantic
**Flujo:**
1. Usuario envía texto: `{"text": "Hola Risp, ¿cómo estás?"}`
2. Backend procesa con Groq para identificar intención y tipo de respuesta
3. Servicio de respuesta valida y formatea la salida
4. Retorna JSON con instrucciones para el frontend
5. Frontend ejecuta la acción correspondiente (mostrar texto, imagen o animación)

## Arquitectura Backend Detallada

### Estructura MVC
- **Models:** Esquemas Pydantic para validación de datos
- **Views:** Representación de respuestas HTTP en JSON
- **Controllers:** Recepción y coordinación de solicitudes
- **Services:** 
  - `groq_service.py` - Comunicación con Groq e interpretación de texto
  - `response_service.py` - Validación y preparación de respuestas
  - `face_service.py` - Lectura, procesamiento y codificación de imágenes (para el endpoint inicial)
- **Repositories:** Consulta del catálogo de recursos disponibles
- **animations/:** Recursos visuales locales para parpadeo (3 variantes con 3 frames cada una)
- **emociones/:** Recursos visuales faciales básicos (para el endpoint inicial)

### Estructura de Carpetas
```text
worship-mascot-robot/
├── emociones/
│   ├── boca/
│   │   └── boca.png
│   ├── nariz/
│   │   └── nariz.png
│   ├── ojo-derecho/
│   │   └── ojo-derecho.png
│   └── ojo-izquierdo/
│       └── ojo-izquierdo.png
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── controllers/
│   │   │   ├── face_controller.py
│   │   │   └── robot_controller.py
│   │   ├── models/
│   │   │   ├── face_component.py
│   │   │   ├── robot_request.py
│   │   │   ├── robot_response.py
│   │   │   └── groq_interpretation.py
│   │   ├── views/
│   │   │   ├── face_view.py
│   │   │   └── robot_view.py
│   │   ├── services/
│   │   │   ├── groq_service.py
│   │   │   ├── response_service.py
│   │   │   └── face_service.py
│   │   ├── repositories/
│   │   │   ├── face_repository.py
│   │   │   └── resource_repository.py
│   │   └── assets/
│   │       └── emociones/
│   │           ├── boca/
│   │           │   └── boca.png
│   │           ├── nariz/
│   │           │   └── nariz.png
│   │           ├── ojo-derecho/
│   │           │   └── ojo-derecho.png
│   │           └── ojo-izquierdo/
│   │               └── ojo-izquierdo.png
│   ├── tests/
│   │   ├── test_face_initial.py
│   │   ├── test_robot_interpret.py
│   │   ├── test_groq_service.py
│   │   └── test_response_service.py
│   ├── docs/
│   │   ├── 01-arquitectura.md
│   │   ├── 02-diagrama-clases.md
│   │   ├── 03-casos-de-uso.md
│   │   ├── 04-flujo-endpoint.md
│   │   └── 05-flujo-usuario.md
│   ├── .env.example
│   │   ├── .gitignore
│   │   └── requirements.txt
└── front-end/  # (por desarrollar)
    └── package.json
```

## Proceso de Interpretación de Texto

1. **Entrada:** Usuario envía texto solicitando una acción o información
2. **Interpretación:** Groq analiza el texto para extraer:
   - `intent`: intención identificada (saludo, mostrar imagen, parpadear, etc.)
   - `response.type`: tipo de salida (text, image o animation)
   - `response.content`: contenido descriptivo de la respuesta
   - `response.resource`: referencia al recurso o parámetros necesarios (cuando aplique)
3. **Validación:** Backend verifica que la intención sea permitida y que los recursos existan
4. **Salida:** JSON con estructura de respuesta para el frontend
5. **Ejecución:** Frontend procesa la respuesta según su tipo (mostrar texto, mostrar imagen o ejecutar animación)

## Proceso de Parpadeo (Caso Específico)

Cuando la intención identificada es "blink":
1. **Entrada:** Usuario envía texto solicitando parpadeo (ej: "Parpadea dos veces")
2. **Interpretación:** Groq identifica:
   - `intent`: "blink"
   - `response.type`: "animation"
   - `response.content`: texto descriptivo (ej: "Voy a parpadear dos veces.")
   - `response.resource`: 
     ```json
     {
       "name": "blink",
       "parameters": {
         "count": 2
       }
     }
     ```
3. **Validación:** Backend verifica que la intención "blink" esté permitida
4. **Salida:** JSON con estructura de animación para el frontend
5. **Ejecución:** Frontend reproduce la animación de parpadeo usando los frames seleccionados

## Seguridad y Validaciones

- Credenciales de Groq almacenadas en variables de entorno (nunca en código)
- Validación rigurosa de entradas con Pydantic
- Límites definidos para cantidad máxima de parpadeos
- Verificación de existencia de recursos antes de referenciarlos
- Manejo controlado de errores de red e inferencia de IA
- Prevención de inyección de comandos mediante instrucciones de IA
- Pruebas exhaustivas para intenciones ambiguas y respuestas inválidas

## Próximos Pasos de Desarrollo

- [ ] Definir e implementar quinto componente facial
- [ ] Crear endpoint para servir componentes faciales iniciales (YA IMPLEMENTADO)
- [ ] Implementar endpoint de interpretación de texto
- [ ] Desarrollar catálogo de animaciones de parpadeo (3 variantes)
- [ ] Integrar con frontend Astro + React para renderizado
- [ ] Establecer WebSocket o mecanismo de eventos para comunicación en tiempo real
- [ ] Preparar documentación de API completa con Swagger/OpenAPI

## Principio de Diseño

**La IA interpreta, el backend coordina y valida, el frontend representa visualmente.** 
Cada responsabilidad evoluciona independientemente mediante contratos bien definidos, evitando acoplamiento innecesario entre componentes.

Esta arquitectura permite:
- Escalabilidad independiente de cada capa
- Reemplazo o actualización de componentes sin afectar otros
- Pruebas unitarias y de integración aisladas
- Mantenimiento y evolución sostenible del sistema