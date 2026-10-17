# 03 — Casos de Uso

## CU-01 Cargar rostro inicial
Actor: Usuario. Abre página → frontend solicita 4 componentes.

## CU-02 Renderizar componentes
Frontend recibe Base64, construye src y muestra boca, nariz, ojos.

## CU-03 Errores de conexión
Sin backend o HTTP no ok → mensaje comprensible.

## CU-04 Respuesta inválida
JSON inválido, success false, datos incompletos → error.

## CU-05 Reintentar
Botón retry vuelve a llamar loadFace.

```mermaid
flowchart LR
  U[Usuario] --> UI[Interfaz] --> E[GET /api/v1/face/initial]
```
