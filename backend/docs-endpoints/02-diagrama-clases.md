# Diagrama de clases y componentes

Las rutas están implementadas como funciones de módulo de FastAPI, no como clases controlador. En el diagrama se representan los módulos de controlador para mostrar sus colaboraciones.

```mermaid
classDiagram
    class FaceController {
        +get_initial_face()
    }
    class FaceService {
        +get_initial_face_components()
    }
    class FaceRepository {
        +get_all_components()
        +get_component_path(component_name)
    }
    class FaceView {
        +create_face_initial_response(success, components)
    }
    class FaceInitialResponse {
        +bool success
        +List~FaceComponent~ components
    }
    class FaceComponent {
        +str name
        +str type
        +str data
    }

    FaceController --> FaceService : coordina
    FaceService --> FaceRepository : solicita componentes
    FaceController --> FaceView : construye respuesta
    FaceView ..> FaceInitialResponse : valida y serializa
    FaceInitialResponse o-- FaceComponent : contiene
```

```mermaid
classDiagram
    class RobotController {
        +interpret_robot_command(request)
    }
    class RobotRequest {
        +str text
    }
    class GroqService {
        +str model
        +interpret_text(request) GroqInterpretation
        +get_blink_frames() List~RobotFrame~
    }
    class GroqInterpretation {
        +Literal intent
        +str content
        +Optional~int~ count
    }
    class ResourceRepository {
        +read_blink_frame_bytes() List
    }
    class RobotResponse {
        +bool success
        +Literal intent
        +RobotResponseData response
    }
    class RobotResponseData {
        +Literal type
        +str content
        +List~RobotFrame~ frames
        +Optional~int~ count
        +validate_response_shape()
    }
    class RobotFrame {
        +str name
        +Literal format
        +str data
    }
    class RobotView {
        +create_robot_response(response)
    }

    RobotController --> RobotRequest : recibe
    RobotController --> GroqService : interpreta
    GroqService ..> GroqInterpretation : valida respuesta de Groq
    GroqService --> ResourceRepository : lee fotogramas
    RobotController ..> RobotResponse : construye
    RobotResponse o-- RobotResponseData : contiene
    RobotResponseData o-- RobotFrame : contiene fotogramas
    RobotController --> RobotView : serializa
```

## Descripción de las clases

### Endpoint `GET /api/v1/face/initial`

- **FaceController:** recibe la solicitud y traduce errores de lectura a estados HTTP.
- **FaceService:** coordina la obtención de los componentes faciales.
- **FaceRepository:** mantiene el catálogo de componentes, lee los PNG y los codifica en Base64.
- **FaceComponent / FaceInitialResponse:** validan la forma de los datos de salida.
- **FaceView:** serializa el modelo de respuesta a JSON.

### Endpoint `POST /api/v1/robot/interpret`

- **RobotRequest:** valida el campo de texto recibido.
- **GroqService:** envía las instrucciones y el mensaje a Groq, valida la intención y codifica fotogramas cuando se solicitan.
- **GroqInterpretation:** admite las intenciones `blink` y `text`, contenido no vacío y una cantidad opcional limitada a 1–10.
- **ResourceRepository:** lee los bytes de `1.png`, `2.png` y `3.png` en ese orden.
- **RobotFrame:** valida cada nombre, formato PNG y contenido Base64 no vacío.
- **RobotResponseData / RobotResponse:** validan los campos de respuesta y que la intención corresponda al tipo (`blink`/`animation`, `text`/`text`).
- **RobotView:** devuelve el modelo validado como JSON.
