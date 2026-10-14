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
- Se envían en grupos de 5 elementos (4 componentes actuales + 1 por definir)
- Proporciona el estado visual base del robot

### 2. Endpoint de Parpadeo
**Propósito:** Interpretar instrucciones de texto y generar acciones de parpadeo
**Endpoint:** `POST /api/v1/robot/interpret`
**Tecnologías:** Python, FastAPI, Groq, Pydantic
**Flujo:**
1. Usuario envía texto: `{"text": "Parpadea dos veces"}`
2. Backend procesa con Groq para identificar intención y cantidad
3. Servicio de animación selecciona variante visual apropiada
4. Retorna JSON con instrucciones de parpadeo
5. Frontend ejecuta la animación correspondiente

## Arquitectura Backend Detallada

### Estructura MVC
- **Models:** Esquemas Pydantic para validación de datos
- **Views:** Representación de respuestas HTTP en JSON
- **Controllers:** Recepción y coordinación de solicitudes
- **Services:** 
  - `groq_service.py` - Comunicación con Groq e interpretación de texto
  - `animation_service.py` - Selección de variantes y validación de cantidad
- **Repositories:** Consulta del catálogo de animaciones disponibles
- **animations/:** Recursos visuales locales para parpadeo (3 variantes con 3 frames cada una)

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
│   │   │   └── robot_controller.py
│   │   ├── models/
│   │   │   ├── robot_request.py
│   │   │   ├── robot_response.py
│   │   │   └── groq_interpretation.py
│   │   ├── views/
│   │   │   └── robot_view.py
│   │   ├── services/
│   │   │   ├── groq_service.py
│   │   │   └── animation_service.py
│   │   ├── repositories/
│   │   │   └── animation_repository.py
│   │   └── animations/
│   │       └── blink/
│   │           ├── variant_01/
│   │           │   ├── frame_01
│   │           │   ├── frame_02
│   │           │   └── frame_03
│   │           │
│   │           ├── variant_02/
│   │           │   ├── frame_01
│   │           │   ├── frame_02
│   │           │   └── frame_03
│   │           │
│   │           └── variant_03/
│   │               ├── frame_01
│   │               ├── frame_02
│   │               └── frame_03
│   ├── tests/
│   ├── .env.example
│   ├── .gitignore
│   └── requirements.txt
└── front-end/  # (por desarrollar)
    └── package.json
```

## Proceso de Parpadeo

1. **Entrada:** Usuario envía texto solicitando parpadeo
2. **Interpretación:** Groq analiza el texto para extraer:
   - `intent`: debe ser "blink"
   - `should_blink`: boolean indicando si se debe parpadear
   - `count`: número de parpadeos solicitados
3. **Validación:** Backend verifica que la intención sea permitida y la cantidad válida
4. **Selección:** Servicio de animación elige una variante visual disponible
5. **Salida:** JSON con estructura de parpadeo para el frontend
6. **Ejecución:** Frontend reproduce la animación de parpadeo usando los frames seleccionados

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
- [ ] Crear endpoint para servir componentes faciales iniciales
- [ ] Implementar endpoint de interpretación de parpadeo
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