# Casos de uso de los endpoints

## Actores

- **Cliente HTTP:** frontend, herramienta de pruebas o consumidor autorizado de la API.
- **Groq:** servicio externo de inferencia usado únicamente por la interpretación de texto.
- **Sistema de archivos del backend:** fuente local de los PNG del rostro y de la animación.

## Caso de uso 1: obtener el rostro inicial

**Identificador:** UC-01  
**Endpoint:** `GET /api/v1/face/initial`

### Precondiciones

- El backend está en ejecución.
- Los cuatro archivos de imagen configurados en `FaceRepository` existen bajo `app/assets/emociones/`.
- El proceso tiene permiso para leer esos archivos.

### Flujo principal

1. El cliente solicita `GET /api/v1/face/initial`.
2. FastAPI llama al controlador del rostro.
3. El controlador solicita al servicio los componentes faciales.
4. El servicio delega la lectura y codificación al repositorio.
5. El repositorio lee y codifica en Base64 los cuatro componentes: `boca`, `nariz`, `ojo-derecho` y `ojo-izquierdo`.
6. La vista valida y serializa la respuesta.
7. El cliente recibe HTTP 200 con `success: true` y la lista `components`.

### Postcondición

El cliente tiene los cuatro PNG codificados como cadenas Base64 para representar el rostro inicial.

### Flujos alternativos

- **Archivo faltante:** el controlador responde HTTP 404.
- **Error de lectura:** el controlador responde HTTP 500.
- **Error inesperado:** el controlador responde HTTP 500.

## Caso de uso 2: interpretar texto y decidir si hay parpadeo

**Identificador:** UC-02  
**Endpoint:** `POST /api/v1/robot/interpret`

### Precondiciones

- El backend está en ejecución.
- `GROQ_API_KEY` está disponible para el backend y el modelo configurado es válido para la cuenta de Groq.
- Para una orden de parpadeo, los archivos `app/assets/ojos/1.png`, `2.png` y `3.png` existen y son legibles.

### Flujo principal

1. El cliente envía un objeto JSON con el campo `text`.
2. FastAPI valida el cuerpo como `RobotRequest`.
3. El controlador solicita a Groq una interpretación estructurada.
4. `GroqService` valida la respuesta con `GroqInterpretation`.
5. Si la intención es `blink`, el servicio lee y codifica los tres fotogramas y el controlador devuelve `type: "animation"` con la cantidad solicitada.
6. Si la intención es `text`, el controlador devuelve el contenido de Groq con `type: "text"` y `frames: []`.
7. Los modelos de salida validan la estructura y la vista la serializa.
8. El cliente recibe HTTP 200.

### Reglas de interpretación

Se le indica a Groq que diferencie una orden afirmativa de una mención sin orden:

| Texto de entrada | Intención esperada |
|---|---|
| `Parpadea` | `blink` |
| `Quiero que parpadees` | `blink` |
| `Haz dos parpadeos` | `blink` |
| `Hola Risp, ¿cómo estás?` | `text` |
| `Explícame qué es parpadear` | `text` |
| `No parpadees` | `text` |
| `¿Puedes parpadear?` | `text` |

La clasificación la produce Groq siguiendo las instrucciones del servicio; no se decide por una búsqueda de palabras dentro del texto.

### Postcondiciones

- La intención `blink` devuelve exactamente tres fotogramas Base64 ordenados y una cantidad de ciclos validada de 1 a 10.
- La intención `text` devuelve el contenido generado por Groq y no incluye datos de imagen.
- No se ejecuta ninguna acción física.

### Flujos alternativos

- **Texto vacío:** el servicio lanza `ValueError`; el controlador responde HTTP 400.
- **Cuerpo JSON inválido o sin el campo requerido:** FastAPI responde HTTP 422.
- **Fallo de Groq, JSON no válido o fallo al leer un fotograma:** el error llega al manejador general del controlador, que responde HTTP 500.
