# Casos de Uso - Backend WORSHIP Mascot Robot

## Actores
- **Frontend Astro + React:** Sistema que solicita los componentes faciales iniciales para renderizar el rostro del robot

## Casos de Uso

### 1. Obtener Componentes Faciales Iniciales
**Descripción:** El frontend solicita los componentes faciales básicos necesarios para renderizar el rostro inicial del robot.

**Actor:** Frontend Astro + React

**Precondiciones:**
- El servidor backend está en ejecución
- Los archivos de imagen PNG existen en la ubicación esperada (`app/assets/emociones/`)
- El servidor tiene permisos de lectura para acceder a los archivos

**Flujo Principal:**
1. El frontend envía una solicitud GET a `/api/v1/face/initial`
2. El backend recibe la solicitud y la enruta al controlador correspondiente
3. El controlador solicita los datos al servicio de componentes faciales
4. El servicio solicita los archivos al repositorio de componentes faciales
5. El repositorio lee cada archivo PNG desde el sistema de archivos
6. El repositorio codifica cada archivo en Base64
7. El repositorio retorna la lista de componentes con sus datos codificados
8. El servicio recibe los datos y los retorna al controlador
9. El controlador utiliza la vista para formatear la respuesta JSON
10. El backend envía la respuesta HTTP 200 con los componentes faciales en formato JSON
11. El frontend recibe la respuesta y decodifica los Base64 para renderizar las imágenes

**Postcondiciones:**
- El frontend tiene todos los componentes faciales necesarios para renderizar el rostro inicial
- Los datos están listos para ser utilizados por el frontend en su proceso de renderización

**Flujos Alternativos:**
- **A1: Archivo faltante** - Si alguno de los archivos PNG no existe:
  - El repositorio lanza una excepción FileNotFoundError
  - El controlador la captura y retorna un error HTTP 404
  - El frontend recibe un mensaje indicando que faltan componentes
  
- **A2: Error de lectura** - Si hay un problema al leer alguno de los archivos:
  - El repositorio lanza una excepción IOError
  - El controlador la captura y retorna un error HTTP 500
  - El frontend recibe un mensaje de error interno del servidor

**Diagrama de Casos de Uso:**
```mermaid
useCaseDiagram
    actor Frontend as "Frontend Astro + React"
    useCase UC1 as "Obtener Componentes Faciales Iniciales"
    
    Frontend --> UC1 : Solicita componentes faciales
    
    %% Límites del sistema
    rectangle Backend {
        UC1
    }
```

## Detalles Técnicos del Caso de Uso Principal

### Endpoint
- **URL:** `/api/v1/face/initial`
- **Método:** GET
- **Headers:** Ninguno requerido
- **Parámetros:** Ninguno

### Respuesta Exitosa (HTTP 200)
```json
{
  "success": true,
  "components": [
    {
      "name": "string",
      "type": "image/png",
      "data": "string (Base64 encoded)"
    }
  ]
}
```

### Respuestas de Error
- **HTTP 404 Not Found:** Cuando falta alguno de los archivos de imagen
  ```json
  {
    "detail": "One or more facial component files are missing"
  }
  ```
  
- **HTTP 500 Internal Server Error:** Cuando hay error al leer los archivos o cualquier otro error inesperado
  ```json
  {
    "detail": "Error reading facial component files"
  }
  ```
  o
  ```json
  {
    "detail": "An unexpected error occurred while processing facial components"
  }
  $$

### Esquema de Datos
Cada componente facial tiene:
- **name:** Identificador único (boca, nariz, ojo-derecho, ojo-izquierdo)
- **type:** Tipo MIME del archivo (siempre "image/png" para esta implementación)
- **data:** Contenido del archivo PNG codificado en Base64