# Arquitectura del Backend WORSHIP Mascot Robot

## Visión General

El backend del WORSHIP Mascot Robot sigue una arquitectura MVC (Modelo-Vista-Controlador) adaptada para una API REST. Esta separación de responsabilidades permite un código más mantenible, testeable y escalable.

## Capas de la Arquitectura

### 1. Modelo (Models)
**Responsabilidad:** Definir la estructura de los datos y realizar validaciones.
- **Ubicación:** `app/models/`
- **Archivo clave:** `face_component.py`
- **Contenido:** 
  - Modelos Pydantic que representan los componentes faciales y la respuesta del endpoint
  - Validación automática de tipos de datos y contraintes

### 2. Vista (Views)
**Responsabilidad:** Formatear la respuesta que se enviará al cliente.
- **Ubicación:** `app/views/`
- **Archivo clave:** `face_view.py`
- **Contenido:** 
  - Funciones que convierten los datos internos en respuestas HTTP apropiadas
  - En este caso, formatear la respuesta JSON con los componentes faciales

### 3. Controlador (Controllers)
**Responsabilidad:** Manejar las solicitudes HTTP y coordinar la interacción entre modelo y vista.
- **Ubicación:** `app/controllers/`
- **Archivo clave:** `face_controller.py`
- **Contenido:** 
  - Definición de rutas API (endpoints)
  - Lógica de manejo de solicitudes y respuestas
  - Gestión de excepciones y códigos de estado HTTP
  - Coordinación entre el service y la view

### 4. Servicio (Services)
**Responsabilidad:** Contener la lógica de negocio del aplicación.
- **Ubicación:** `app/services/`
- **Archivo clave:** `face_service.py`
- **Contenido:** 
  - Operaciones relacionadas con el procesamiento de componentes faciales
  - Coordinación con el repositorio para obtener datos
  - Preparación de datos para ser presentados por la vista

### 5. Repositorio (Repositories)
**Responsabilidad:** Abstraer el acceso a fuentes de datos (en este caso, sistema de archivos).
- **Ubicación:** `app/repositories/`
- **Archivo clave:** `face_repository.py`
- **Contenido:** 
  - Métodos para acceder a los archivos de imagen en el sistema de archivos
  - Lectura y codificación de archivos PNG a Base64
  - Manejo de errores de acceso a archivos
  - Abstracción de los detalles de almacenamiento

### 6. Main
**Responsabilidad:** Inicializar la aplicación FastAPI y configurar el enrutamiento.
- **Ubicación:** `app/main.py`
- **Contenido:** 
  - Creación de la instancia de FastAPI
  - Registro de routers
  - Configuración básica de la aplicación

## Flujo de Datos

1. El cliente envía una solicitud HTTP GET a `/api/v1/face/initial`
2. FastAPI enruta la solicitud al `FaceController`
3. El controlador llama al `FaceService` para obtener los componentes
4. El servicio solicita los datos al `FaceRepository`
5. El repositorio lee los archivos del sistema de archivos y los codifica en Base64
6. Los datos retornan a través de las capas: repositorio → servicio → controlador
7. El controlador usa la `FaceView` para formatear la respuesta JSON
8. FastAPI envía la respuesta al cliente

## Beneficios de esta Arquitectura

- **Separación de preocupaciones:** Cada capa tiene una responsabilidad clara y definida
- **Testabilidad:** Cada componente puede ser probado de forma aislada
- **Mantenibilidad:** Los cambios en una capa tienen mínimo impacto en las otras
- **Escalabilidad:** Nuevas funcionalidades pueden añadirse siguiendo el mismo patrón
- **Reusabilidad:** Componentes como el repositorio pueden ser reutilizados en otros contextos