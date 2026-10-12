# WORSHIP Mascot Robot — Backend

**Microservicio 01: Emotion & Text**

Backend encargado de interpretar instrucciones de texto mediante Groq y convertirlas en acciones estructuradas para la mascota robótica de WORSHIP.

## 1. Objetivo

Construir un microservicio independiente con FastAPI y arquitectura MVC que reciba texto en formato JSON, identifique la intención del usuario y determine si debe ejecutarse una acción de parpadeo.

La primera funcionalidad será:

**Texto de entrada → Groq → interpretación de intención → selección de animación → respuesta JSON.**

El backend no renderiza animaciones ni controla directamente la interfaz. Devuelve los datos necesarios para que el frontend Astro + React ejecute la expresión correspondiente.

## 2. Tecnologías

- **Python:** lenguaje principal.
- **FastAPI:** API REST.
- **Groq:** inferencia del modelo de IA.
- **Pydantic:** validación de solicitudes y respuestas.
- **Uvicorn:** servidor de desarrollo.
- **python-dotenv:** gestión de variables de entorno.

## 3. Funcionamiento del servicio

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

### Ejemplo de interpretación

Entrada:

```json
{
  "text": "Quiero que parpadees dos veces"
}
```

La IA deberá identificar:

- `intent`: parpadear.
- `should_blink`: `true`.
- `count`: `2`.

Si el usuario solicita una acción no relacionada con el parpadeo, el servicio deberá indicarlo sin seleccionar una animación de forma incorrecta.

## 4. Selección de animaciones

Los recursos visuales estarán organizados en tres carpetas independientes, cada una con tres archivos de animación basados en iframes.

Estructura conceptual:

```text
animations/
└── blink/
    ├── variant_01/
    │   ├── frame_01
    │   ├── frame_02
    │   └── frame_03
    │
    ├── variant_02/
    │   ├── frame_01
    │   ├── frame_02
    │   └── frame_03
    │
    └── variant_03/
        ├── frame_01
        ├── frame_02
        └── frame_03
```

Los nombres son ilustrativos y podrán ajustarse a los archivos reales.

El backend consultará el catálogo de animaciones y seleccionará una variante válida. Cada variante tendrá una referencia identificable que el frontend utilizará para reproducirla.

**Importante:** la cantidad de parpadeos solicitada y la variante visual son conceptos distintos. La cantidad determina cuántas veces se ejecuta la acción; la variante determina qué secuencia visual se utiliza.

## 5. Arquitectura MVC

Se utilizará MVC adaptado a una API REST, separando las responsabilidades de entrada, lógica y datos.

- **Models:** esquemas Pydantic para validar las solicitudes, las interpretaciones y las respuestas.
- **Views:** representación de las respuestas HTTP en formato JSON.
- **Controllers:** recepción de solicitudes y coordinación del flujo de ejecución.
- **Services:** integración con Groq y selección de animaciones.

Los servicios no deben contener lógica de presentación y los controladores no deben comunicarse directamente con el modelo de IA si esa responsabilidad ya está encapsulada en `GroqService`.

## 6. Estructura del backend

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
│           ├── variant_02/
│           └── variant_03/
│
├── tests/
│   ├── test_robot_controller.py
│   └── test_animation_service.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

### Responsabilidad de cada módulo

| Módulo | Responsabilidad |
|---|---|
| `main.py` | Inicialización de FastAPI y registro de rutas |
| `controllers/` | Recepción y coordinación de solicitudes |
| `models/` | Validación de datos y contratos JSON |
| `views/` | Construcción de respuestas HTTP |
| `services/groq_service.py` | Comunicación con Groq e interpretación del texto |
| `services/animation_service.py` | Selección de la variante y validación de la cantidad |
| `repositories/` | Consulta del catálogo de animaciones disponibles |
| `animations/` | Recursos visuales locales |
| `tests/` | Pruebas del comportamiento del servicio |

## 7. API inicial

### `POST /api/v1/robot/interpret`

Recibe texto y devuelve la interpretación junto con la acción y la referencia visual seleccionada.

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

Los identificadores anteriores son ejemplos del contrato; el servicio deberá devolver los recursos que realmente existan en el catálogo.

Si el texto no solicita un parpadeo, una respuesta posible sería:

```json
{
  "success": true,
  "intent": "other",
  "should_blink": false,
  "count": 0,
  "animation": null
}
```

Las solicitudes inválidas deberán producir errores HTTP apropiados. Los fallos de Groq deberán tratarse de manera controlada, sin inventar una interpretación ni ejecutar una animación por defecto.

## 8. Integración con Groq

Groq será el servicio de inferencia utilizado para interpretar las instrucciones.

El modelo recibirá el texto del usuario y deberá producir una salida estructurada con la intención identificada y la cantidad solicitada.

La respuesta de la IA no se considerará confiable automáticamente: el backend validará que la intención esté permitida, que la cantidad sea un entero dentro de los límites configurados y que exista una animación compatible.

La clave de Groq se almacenará en una variable de entorno:

```env
GROQ_API_KEY=tu_clave_de_groq
```

El archivo `.env` no debe subirse al repositorio. Se incluirá `.env.example` con los nombres de las variables, sin credenciales reales.

## 9. Instalación y ejecución

Se recomienda Python 3.11 o superior, verificando la compatibilidad de las dependencias elegidas.

### Crear entorno virtual

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

### Instalar dependencias

```bash
pip install -r requirements.txt
```

### Configurar las variables de entorno

Crear un archivo `.env` en la raíz de `backend/` y configurar `GROQ_API_KEY`.

### Iniciar FastAPI

Desde la carpeta `backend/`:

```bash
uvicorn app.main:app --reload
```

La documentación interactiva estará disponible en:

- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/redoc`

## 10. Seguridad y validaciones

- Mantener la clave de Groq fuera del código fuente.
- Validar las entradas con Pydantic.
- Limitar la cantidad máxima de parpadeos.
- Comprobar que las variantes y los recursos existan.
- Tratar los errores de red y de inferencia.
- No permitir que el modelo invente rutas o ejecute archivos.
- No aceptar instrucciones de IA como comandos directos de hardware.
- Añadir pruebas para intenciones ambiguas y respuestas inválidas.

## 11. Alcance de la primera versión

- [ ] Crear la aplicación FastAPI.
- [ ] Implementar la estructura MVC.
- [ ] Definir los modelos de entrada y salida.
- [ ] Integrar Groq.
- [ ] Interpretar si el usuario solicita parpadear.
- [ ] Determinar la cantidad de parpadeos.
- [ ] Crear el catálogo de las tres variantes visuales.
- [ ] Devolver una variante existente en JSON.
- [ ] Probar la API con Swagger.
- [ ] Preparar la integración con Astro + React.

## 12. Evolución futura

Este microservicio será la primera unidad independiente de la arquitectura de WORSHIP Mascot Robot.

En etapas posteriores, otros servicios podrán encargarse de vídeo y visión artificial, movimientos, ruedas, motores y sensores. La comunicación se diseñará mediante contratos definidos, evitando acoplar la interpretación del texto con el control físico del robot.

**Principio de diseño:** Groq interpreta, FastAPI coordina, el catálogo identifica los recursos y el frontend ejecuta la animación.