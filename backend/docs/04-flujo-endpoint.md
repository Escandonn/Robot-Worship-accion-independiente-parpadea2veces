# Flujo del Endpoint - Backend WORSHIP Mascot Robot

## Descripción
Este documento muestra el flujo detallado de cómo una solicitud HTTP atraviesa todas las capas del backend hasta generar la respuesta JSON, así como el flujo de manejo de errores.

## Flujo de Éxito (Secuencia Normal)

```mermaid
sequenceDiagram
    participant F as Frontend
    participant FA as FastAPI
    participant C as FaceController
    participant S as FaceService
    participant R as FaceRepository
    participant FS as Sistema de Archivos
    
    F->>FA: GET /api/v1/face/initial
    FA->>C: Enruta a FaceController.get_initial_face()
    C->>S: Llama a face_service.get_initial_face_components()
    S->>R: Llama a repository.get_all_components()
    
    loop Para cada componente (boca, nariz, ojo-derecho, ojo-izquierdo)
        R->>FS: Abre archivo [nombre].png
        FS-->>R: Retorna contenido binario
        R->>R: Codifica contenido a Base64
    end
    
    R-->>S: Retorna lista de componentes con datos Base64
    S-->>C: Retorna lista de componentes
    C->>FA: Llama a FaceView.create_face_initial_response()
    FA-->>F: HTTP 200 OK con JSON de componentes
```

## Flujo de Error - Archivo Faltante

```mermaid
sequenceDiagram
    participant F as Frontend
    participant FA as FastAPI
    participant C as FaceController
    participant S as FaceService
    participant R as FaceRepository
    participant FS as Sistema de Archivos
    
    F->>FA: GET /api/v1/face/initial
    FA->>C: Enruta a FaceController.get_initial_face()
    C->>S: Llama a face_service.get_initial_face_components()
    S->>R: Llama a repository.get_all_components()
    
    R->>FS: Intenta abrir archivo faltante.png
    FS-->>R: Lanza excepción FileNotFoundError
    R->>R: Captura y relanza como FileNotFoundError
    S-->>C: Propaga excepción FileNotFoundError
    C->>FA: Captura excepción y retorna HTTP 404
    FA-->>F: HTTP 404 Not Found con mensaje de error
```

## Flujo de Error - Error de Lectura

```mermaid
sequenceDiagram
    participant F as Frontend
    participant FA as FastAPI
    participant C as FaceController
    participant S as FaceService
    participant R as FaceRepository
    participant FS as Sistema de Archivos
    
    F->>FA: GET /api/v1/face/initial
    FA->>C: Enruta a FaceController.get_initial_face()
    C->>S: Llama a face_service.get_initial_face_components()
    S->>R: Llama a repository.get_all_components()
    
    R->>FS: Intenta leer archivo.png
    FS-->>R: Lanza excepción IOError (permiso, disco dañado, etc.)
    R->>R: Captura y relanza como IOError
    S-->>C: Propaga excepción IOError
    C->>FA: Captura excepción y retorna HTTP 500
    FA-->>F: HTTP 500 Internal Server Error con mensaje de error
```

## Flujo de Error - Error Inesperado

```mermaid
sequenceDiagram
    participant F as Frontend
    participant FA as FastAPI
    participant C as FaceController
    participant S as FaceService
    participant R as FaceRepository
    
    F->>FA: GET /api/v1/face/initial
    FA->>C: Enruta a FaceController.get_initial_face()
    C->>S: Llama a face_service.get_initial_face_components()
    S->>R: Llama a repository.get_all_components()
    
    R-->>S: Retorna datos válidos
    S-->>C: Durante el procesamiento, ocurre excepción inesperada
    S->>C: Propaga excepción genérica
    C->>FA: Captura excepción y retorna HTTP 500
    FA-->>F: HTTP 500 Internal Server Error con mensaje genérico
```

## Detalles de Cada Capa en el Flujo de Éxito

### 1. FastAPI → FaceController
- FastAPI recibe la solicitud HTTP
- La enruta al método apropiado basado en el path y método HTTP
- Inyecta automáticamente cualquier dependencia declarada

### 2. FaceController → FaceService
- El controlador valida que el servicio esté disponible
- Llama al método de servicio para obtener los datos de negocio
- Maneja cualquier excepción que pueda lanzar el servicio

### 3. FaceService → FaceRepository
- El servicio coordina la obtención de datos
- Delegar la responsabilidad de acceso a datos al repositorio
- No contiene lógica de acceso directo a archivos

### 4. FaceRepository → Sistema de Archivos
- El repositorio implementa el acceso real a los datos
- Lee los archivos físicos desde el disco
- Codifica los datos binarios a Base64 para transporte seguro en JSON
- Maneja errores específicos de acceso a archivos

### 5. FaceRepository → FaceService
- Retorna los datos procesados en el formato esperado
- Los errores se propagan como excepciones para ser manejados por capas superiores

### 6. FaceService → FaceController
- Retorna los datos de negocio al controlador
- Mantiene la separación entre lógica de negocio y manejo HTTP

### 7. FaceController → FaceView → FastAPI
- El controlador delega la formateo de la respuesta a la vista
- La vista crea el objeto de respuesta apropiado
- FastAPI serializa la respuesta y la envía al cliente