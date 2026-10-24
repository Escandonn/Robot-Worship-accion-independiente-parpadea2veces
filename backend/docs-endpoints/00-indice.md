# Documentación de los endpoints del backend

Esta carpeta documenta los dos endpoints funcionales del backend WORSHIP Mascot Robot. Los documentos se crean como complemento; los archivos de `backend/docs/` no se modifican.

## Documentos

1. [Arquitectura](01-arquitectura.md): capas y responsabilidades de ambos flujos.
2. [Diagrama de clases](02-diagrama-clases.md): modelos y componentes que colaboran por endpoint.
3. [Casos de uso](03-casos-de-uso.md): actores, precondiciones, flujos y resultados esperados.
4. [Flujo de endpoints](04-flujo-endpoints.md): secuencias de éxito y error.
5. [Flujo de usuario](05-flujo-usuario.md): interacción desde la perspectiva del cliente.
6. [Referencia técnica de la API](06-referencia-tecnica-api.md): métodos, rutas, esquemas, ejemplos y errores.

## Endpoints cubiertos

| Método | Ruta | Propósito |
|---|---|---|
| `GET` | `/api/v1/face/initial` | Obtener los cuatro componentes del rostro inicial codificados en Base64. |
| `POST` | `/api/v1/robot/interpret` | Interpretar un texto con Groq y responder con texto o con los fotogramas del parpadeo. |

Los diagramas describen el comportamiento implementado en el backend. El cliente consume el JSON; la ejecución de animaciones y cualquier control físico quedan fuera del alcance.
