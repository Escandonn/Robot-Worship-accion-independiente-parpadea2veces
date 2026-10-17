# 04 — Flujo Endpoint

Método: GET. Ruta: `/api/v1/face/initial`. Base: `PUBLIC_API_BASE_URL`.

URL final: `http://127.0.0.1:8000/api/v1/face/initial`.

Service ejecuta fetch, comprueba `response.ok`, parsea JSON, valida `success`, array de 4, cada componente name/type/data. Entrega a controller, actualiza estado React, FaceRenderer construye `data:${type};base64,${data}`.

Errores: conexión, HTTP, JSON, success, componentes.

Ejemplo respuesta como contrato (Base64 ilustrativo).

```mermaid
sequenceDiagram
  participant U as Usuario
  participant V as FaceView
  participant C as Controller
  participant S as Service
  participant B as Backend
  U->>V: montaje
  V->>C: loadFace
  C->>S: fetchFaceInitial
  S->>B: GET /api/v1/face/initial
  B-->>S: JSON
  S-->>C: FaceResponse
  C-->>V: data
  V->>V: FaceRenderer
```
