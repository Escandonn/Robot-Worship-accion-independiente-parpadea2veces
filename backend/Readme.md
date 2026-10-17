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
4. Iniciar el servidor: `python -m uvicorn app.main:app --reload`
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

## 8. Segundo Endpoint: Interpretación de Texto mediante IA

## 1. Visión general

Este microservicio backend interpreta instrucciones en lenguaje natural para determinar qué respuesta debe generar la mascota robótica WORSHIP.

El servicio recibe un texto mediante una solicitud HTTP, lo procesa utilizando un modelo de inteligencia artificial de Groq y devuelve un JSON estructurado que indica el tipo de respuesta que debe ejecutar o representar el frontend Astro + React.

La respuesta puede corresponder a:

- **Imagen:** seleccionar o solicitar la representación de un recurso visual.
- **Animación:** indicar una acción visual que el frontend pueda ejecutar.
- **Texto:** generar una respuesta textual para comunicarla al usuario.

Este endpoint funciona como una capa de interpretación entre el lenguaje natural y las capacidades visuales de la mascota. No ejecuta directamente las animaciones ni controla los componentes físicos del robot.

## 2. Objetivo

Convertir instrucciones en lenguaje natural en respuestas estructuradas y validadas, listas para que el frontend determine cómo representarlas.

Ejemplo de entrada:

```json
{
  "text": "Hola Risp, ¿cómo estás?"
}
```

La IA analiza la instrucción y devuelve una respuesta cuyo tipo puede ser `text`, `image` o `animation`, junto con los datos correspondientes.

## 3. Tecnologías

- **Python:** lenguaje principal.
- **FastAPI:** API REST.
- **Groq:** inferencia del modelo de inteligencia artificial.
- **Pydantic:** validación de solicitudes y respuestas.
- **Uvicorn:** servidor de desarrollo.
- **python-dotenv:** gestión de variables de entorno.
- **JSON:** formato de comunicación entre el frontend y el backend.

## 4. Endpoint de interpretación

### 4.1 Ruta

```http
POST /api/v1/robot/interpret
```

### 4.2 Solicitud

El endpoint recibe un objeto JSON con el texto enviado por el usuario.

```json
{
  "text": "Hola Risp, ¿cómo estás?"
}
```

El campo `text` es obligatorio y debe contener una cadena no vacía.

### 4.3 Funcionamiento de la IA

Groq debe interpretar el mensaje e identificar:

1. La intención principal del usuario.
2. El contenido de la respuesta.
3. El tipo de salida más apropiado.
4. Los datos necesarios para que el frontend represente la respuesta.

La IA debe producir una salida estructurada que cumpla el esquema definido por el backend. El backend debe validar esa salida antes de devolverla al frontend.

### 4.4 Respuesta para texto

Solicitud:

```json
{
  "text": "Hola Risp, ¿cómo estás?"
}
```

Respuesta de ejemplo:

```json
{
  "success": true,
  "intent": "greeting",
  "response": {
    "type": "text",
    "content": "¡Hola! Estoy listo para ayudarte.",
    "resource": null
  }
}
```

### 4.5 Respuesta para imagen

Si la instrucción requiere una imagen, la respuesta debe indicar ese tipo de salida y proporcionar una referencia al recurso correspondiente.

```json
{
  "success": true,
  "intent": "show_image",
  "response": {
    "type": "image",
    "content": "Aquí tienes la imagen solicitada.",
    "resource": {
      "name": "imagen-ejemplo",
      "path": "emociones/imagen-ejemplo.png"
    }
  }
}
```

Este ejemplo define el contrato esperado. El recurso debe existir en el catálogo que implemente el backend. No se deben inventar rutas ni devolver archivos inexistentes.

### 4.6 Respuesta para animación

Si el usuario solicita una acción visual, la IA puede clasificarla como una animación.

```json
{
  "success": true,
  "intent": "blink",
  "response": {
    "type": "animation",
    "content": "Voy a parpadear dos veces.",
    "resource": {
      "name": "blink",
      "parameters": {
        "count": 2
      }
    }
  }
}
```

Esta respuesta únicamente identifica la acción solicitada. La ejecución real de la animación corresponderá al sistema encargado de administrar los recursos visuales del robot.

### 4.7 Contrato común de respuesta

Todas las respuestas deben mantener una estructura consistente:

- `success`: indica si el procesamiento terminó correctamente.
- `intent`: intención identificada por el modelo.
- `response.type`: tipo de salida (`text`, `image` o `animation`).
- `response.content`: texto descriptivo o contenido textual de la respuesta.
- `response.resource`: referencia y parámetros del recurso, o `null` cuando no sean necesarios.

Los valores de `intent` deben estar definidos en el modelo de datos del backend. No se debe confiar directamente en campos generados por la IA sin validarlos.

## 5. Arquitectura MVC

Se mantiene la arquitectura MVC adaptada a FastAPI, con una separación adicional de servicios para integrar la IA.

### Models

Ubicación: `app/models/`

Responsabilidades:

- Validar el texto recibido.
- Definir los tipos de respuesta permitidos.
- Validar la intención y los datos asociados.
- Definir el contrato JSON de salida.

Archivos propuestos:

- `robot_request.py`
- `robot_response.py`
- `groq_interpretation.py`

### Views

Ubicación: `app/views/`

Archivo:

- `robot_view.py`

Responsabilidad: preparar la representación JSON de la respuesta que recibirá el frontend.

### Controllers

Ubicación: `app/controllers/`

Archivo:

- `robot_controller.py`

Responsabilidades:

- Recibir la solicitud HTTP.
- Validar los datos de entrada mediante los modelos.
- Coordinar el servicio de interpretación.
- Entregar la respuesta validada.
- Gestionar los errores HTTP.

### Services

Ubicación: `app/services/`

Archivos:

- `groq_service.py`
- `response_service.py`

`groq_service.py` se encarga de comunicarse con Groq y obtener la interpretación estructurada.

`response_service.py` valida la interpretación, determina el tipo de salida y coordina la preparación de la respuesta.

La lógica de negocio no debe estar concentrada en el controller.

### Repositories

Ubicación: `app/repositories/`

Archivo:

- `resource_repository.py`

Responsabilidad: consultar el catálogo de recursos disponibles y comprobar qué imágenes o animaciones están registradas.

Si la respuesta es de tipo texto y no necesita recursos, no será necesario consultar el repositorio.

### Main

Ubicación: `app/main.py`

Responsabilidades:

- Inicializar FastAPI.
- Registrar las rutas del controller.
- Configurar los elementos comunes de la aplicación.
- Proporcionar el punto de entrada para Uvicorn.

## 6. Estructura del backend

```text
backend/
├── app/
│   ├── main.py
│   ├── controllers/
│   │   └── robot_controller.py
│   ├── models/
│   │   ├── robot_request.py
│   │   ├── robot_response.py
│   │   └── groq_interpretation.py
│   ├── views/
│   │   └── robot_view.py
│   ├── services/
│   │   ├── groq_service.py
│   │   └── response_service.py
│   ├── repositories/
│   │   └── resource_repository.py
│   └── assets/
│       └── emociones/
├── tests/
│   ├── test_robot_interpret.py
│   ├── test_groq_service.py
│   └── test_response_service.py
├── docs/
│   ├── 01-arquitectura.md
│   ├── 02-diagrama-clases.md
│   ├── 03-casos-de-uso.md
│   ├── 04-flujo-endpoint.md
│   └── 05-flujo-usuario.md
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

La carpeta `assets/` puede reutilizarse para consultar los recursos del rostro inicial, pero la implementación debe mantener separado el endpoint de rostro base del endpoint de interpretación.

## 7. Flujo de funcionamiento

```text
Usuario
   |
   | Envía texto en JSON
   v
Frontend Astro + React
   |
   | POST /api/v1/robot/interpret
   v
FastAPI
   |
   v
RobotController
   |
   v
GroqService
   |
   | Envía instrucciones y texto a Groq
   v
Modelo de IA
   |
   | Devuelve interpretación estructurada
   v
ResponseService
   |
   | Valida intención y tipo de salida
   |
   +------> Texto
   |
   +------> Imagen
   |
   +------> Animación
   |
   v
ResourceRepository (cuando corresponda)
   |
   v
RobotResponse — Pydantic
   |
   v
RobotView
   |
   v
Respuesta JSON
   |
   v
Frontend Astro + React
   |
   v
Representación visual o textual
```

## 8. Integración con Groq

La clave de acceso debe almacenarse en una variable de entorno.

Archivo `.env`:

```env
GROQ_API_KEY=tu_clave_de_groq
GROQ_MODEL=tu_modelo_disponible
```

El nombre del modelo debe corresponder a un modelo disponible en la cuenta de Groq.

El servicio de IA debe:

1. Recibir el texto validado.
2. Construir las instrucciones para obtener una interpretación estructurada.
3. Solicitar la respuesta al modelo configurado.
4. Procesar la salida recibida.
5. Validar que la respuesta cumpla el esquema esperado.
6. Devolver una interpretación al servicio de respuesta.

Si Groq devuelve contenido inválido, la solicitud falla o se agota el tiempo de espera, el backend debe gestionar el error de forma controlada.

La clave API nunca debe enviarse al frontend ni incluirse en el repositorio.

## 9. Instalación y ejecución

Crear el entorno virtual:

```bash
python -m venv .venv
```

Activar en Windows:

```powershell
.venv\Scripts\activate
```

Activar en Linux/macOS:

```bash
source .venv/bin/activate
```

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

Configurar el archivo `.env` a partir de `.env.example` y establecer las variables necesarias.

Iniciar el backend:

```bash
uvicorn app.main:app --reload
```

Documentación interactiva:

- Swagger: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

Para probar el endpoint, enviar una solicitud `POST` a:

```text
http://127.0.0.1:8000/api/v1/robot/interpret
```

Con el encabezado `Content-Type: application/json` y un cuerpo JSON válido.

## 10. Seguridad y validaciones

- Validar el texto de entrada con Pydantic.
- Establecer límites razonables de longitud para el texto.
- Limitar los tipos de salida permitidos.
- Validar toda respuesta recibida de Groq.
- No permitir que la IA determine rutas arbitrarias del sistema de archivos.
- Resolver los recursos mediante un catálogo controlado.
- Configurar tiempos de espera para las solicitudes a Groq.
- Manejar errores de conexión, límites de uso y respuestas inválidas.
- Mantener las claves y variables sensibles fuera del código fuente.
- No exponer mensajes internos, trazas ni credenciales al cliente.
- Probar los servicios con respuestas simuladas para evitar depender de Groq en todas las pruebas.

## 11. Documentación técnica obligatoria

Crear los siguientes archivos Markdown independientes dentro de `docs/`:

- `01-arquitectura.md`: descripción de la arquitectura y responsabilidades de las capas, con diagrama de componentes Mermaid.
- `02-diagrama-clases.md`: clases, atributos, métodos y relaciones mediante Mermaid.
- `03-casos-de-uso.md`: actores, casos de uso, precondiciones y alternativas.
- `04-flujo-endpoint.md`: diagrama de secuencia desde la recepción del texto hasta la respuesta JSON.
- `05-flujo-usuario.md`: flujo de interacción entre el usuario, la interfaz y la mascota, incluyendo estados de éxito y error.

Los diagramas deben corresponder a los archivos y responsabilidades implementados realmente.

## 12. Pruebas automatizadas

Implementar pruebas para comprobar:

- Solicitud válida con respuesta de tipo `text`.
- Solicitud que genera una respuesta de tipo `image`.
- Solicitud que identifica una acción de tipo `animation`.
- Texto vacío o inválido.
- Respuesta de Groq con formato incorrecto.
- Error de conexión o tiempo de espera de Groq.
- Recurso visual inexistente.
- Intención no reconocida.
- Validación de los campos del JSON de salida.

Las pruebas unitarias deben poder ejecutarse sin llamar al servicio real de Groq, utilizando mocks cuando corresponda.

## 13. Próximos pasos

- [ ] Implementar el endpoint `POST /api/v1/robot/interpret`.
- [ ] Implementar la integración con Groq.
- [ ] Definir los modelos Pydantic de entrada y salida.
- [ ] Implementar la clasificación de respuestas `text`, `image` y `animation`.
- [ ] Crear el catálogo de recursos visuales.
- [ ] Crear los cinco documentos técnicos con diagramas Mermaid.
- [ ] Implementar pruebas automatizadas.
- [ ] Integrar el endpoint con Astro + React.
- [ ] Preparar la extensión hacia el microservicio de parpadeo y las futuras emociones del robot.

## 14. Criterio de finalización

El endpoint estará listo cuando reciba texto mediante JSON, obtenga una interpretación de Groq, valide la salida y devuelva una respuesta estructurada que el frontend pueda procesar sin tener que interpretar nuevamente el lenguaje natural.

El endpoint debe actuar como una capa de interpretación y preparación de respuestas, manteniendo desacopladas la IA, los recursos visuales, la presentación del frontend y la futura ejecución de acciones físicas del robot.

## 9. Próximos Pasos

- [ ] Implementar pruebas automatizadas completas
- [ ] Añadir documentación detallada en los archivos de docs/
- [ ] Preparar integración con frontend Astro + React
- [ ] Diseñar estructura para futuros endpoints (parpadeo, emociones, etc.)