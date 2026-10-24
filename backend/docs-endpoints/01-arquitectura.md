# Arquitectura de los endpoints

## Propósito

Este documento describe cómo se organizan las capas MVC del backend para `GET /api/v1/face/initial` y `POST /api/v1/robot/interpret`. Complementa la documentación existente en `backend/docs/` sin modificarla.

## Componentes y responsabilidades

| Capa | Ubicación | Responsabilidad |
|---|---|---|
| Inicialización y rutas | `app/main.py` | Crea la aplicación FastAPI y registra los routers de rostro y robot. |
| Controlador | `app/controllers/` | Recibe la solicitud, coordina los servicios y convierte errores en respuestas HTTP. |
| Modelo | `app/models/` | Valida los datos de solicitud, las interpretaciones de Groq y las respuestas JSON. |
| Servicio | `app/services/` | Coordina la lógica de negocio; el servicio Groq interpreta el texto y codifica fotogramas. |
| Repositorio | `app/repositories/` | Lee los recursos de imagen disponibles en el sistema de archivos. |
| Vista | `app/views/` | Construye la respuesta JSON a partir de los modelos validados. |
| Recursos | `app/assets/` | Contiene los PNG del rostro inicial y los tres fotogramas de parpadeo. |

## Flujo del rostro inicial

1. FastAPI enruta `GET /api/v1/face/initial` a `face_controller.get_initial_face`.
2. El controlador solicita los componentes a `FaceService`.
3. `FaceService` delega la lectura a `FaceRepository`.
4. El repositorio lee los PNG de `app/assets/emociones/` y codifica sus bytes en Base64.
5. El controlador entrega los datos a `create_face_initial_response`.
6. La vista valida `FaceInitialResponse` y responde con JSON.

## Flujo de interpretación del robot

1. FastAPI valida el cuerpo de `POST /api/v1/robot/interpret` mediante `RobotRequest`.
2. `robot_controller.interpret_robot_command` llama a `GroqService.interpret_text`.
3. `GroqService` envía el texto y las instrucciones de clasificación a Groq, valida el JSON recibido con `GroqInterpretation` y obtiene una intención (`blink` o `text`).
4. Para `blink`, el controlador solicita los fotogramas al servicio. Este lee `1.png`, `2.png` y `3.png` desde `app/assets/ojos/` usando `ResourceRepository` y codifica cada imagen en Base64.
5. Para `text`, el controlador conserva el contenido devuelto por Groq y no lee fotogramas.
6. El controlador construye `RobotResponse`; los modelos validan la correspondencia entre intención y tipo de respuesta.
7. `create_robot_response` serializa el modelo validado a JSON.

## Reglas de datos de parpadeo

- Solo una interpretación afirmativa clasificada como `blink` produce `type: "animation"`.
- Las preguntas, negaciones y explicaciones se clasifican como `text` de acuerdo con las instrucciones enviadas a Groq.
- La cantidad de ciclos admitida es un entero de 1 a 10.
- Cada animación contiene exactamente tres fotogramas PNG, en orden: `1.png`, `2.png`, `3.png`.
- Una respuesta textual contiene `frames: []` y no lleva una cantidad de ciclos.

## Límites del sistema

- No se ejecutan movimientos físicos ni se controla hardware.
- El endpoint de rostro inicial y el endpoint de interpretación tienen responsabilidades independientes.
- Las imágenes no se copian ni se transforman en archivos nuevos; se leen y codifican al procesar cada solicitud.
