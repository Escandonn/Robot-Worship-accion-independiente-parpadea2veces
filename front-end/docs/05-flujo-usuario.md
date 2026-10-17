# 05 — Flujo Usuario

Estados: loading, success, error.

Inicio → cargar página → montar React → solicitar endpoint → ¿válido? Sí → renderizar rostro → fin. No → error → retry (si implementado).

Backend desconectado → error + retry.

```mermaid
flowchart TD
  A[Inicio] --> B[Cargar página]
  B --> C[Solicitar endpoint]
  C --> D{Respuesta válida?}
  D -- Sí --> E[Renderizar rostro]
  D -- No --> F[Mostrar error]
  F --> G[Reintentar]
```
