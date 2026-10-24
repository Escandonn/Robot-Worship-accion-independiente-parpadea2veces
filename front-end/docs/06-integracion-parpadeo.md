# 06 — Integración visual del parpadeo

## Alcance

Este documento complementa la arquitectura existente del frontend. La funcionalidad reutiliza el flujo MVC, los componentes React actuales y el endpoint `POST /api/v1/robot/interpret`; no introduce una arquitectura alternativa ni controla hardware. La base de API predeterminada es `https://robot-worship-accion-independiente.vercel.app` y puede sobrescribirse mediante `PUBLIC_API_BASE_URL`.

## Flujo de integración

1. `ChatCentral` envía el texto mediante `chatController` y `chatService`.
2. `chatService` valida la respuesta discriminada (`text` o `blink`), incluidos el orden de los tres PNG y el límite de ciclos.
3. Si la intención es `blink`, `ChatCentral` avisa a `FaceView` con los fotogramas Base64 y la cantidad de ciclos.
4. `FaceView` pasa la animación a `FaceRenderer`.
5. `FaceRenderer` muestra los tres fotogramas en secuencia y repite el ciclo indicado. El último `3.png` permanece dos segundos adicionales y muestra un globo con el mensaje «YA ERES PARTE DE WORSHIP». Después restaura las imágenes originales del rostro.

## Preservación de la posición y tamaño de ojos

Los PNG del parpadeo se utilizan como fuentes temporales para los dos elementos `<img>` que ya representan los ojos. No se añaden elementos nuevos ni se modifican sus reglas CSS.

Las posiciones, anchuras y alturas se siguen tomando de `src/config/faceLayout.ts`:

| Ojo | X | Y | Ancho | Alto |
|---|---:|---:|---:|---:|
| `ojo-izquierdo` | -17% | 12% | 72% | 62% |
| `ojo-derecho` | 44% | 12% | 72% | 62% |

El estilo inline existente se mantiene durante todos los fotogramas; al terminar, cada ojo vuelve a usar su Base64 original del endpoint facial.

Mientras los ojos están visibles, un resplandor rojo y dorado crea un halo alrededor de sus píxeles transparentes. El fotograma cerrado añade un brillo violeta más intenso; el globo aparece únicamente durante ese fotograma. Las animaciones decorativas respetan `prefers-reduced-motion`.

## Contrato esperado del endpoint

Una orden de parpadeo debe devolver `intent: "blink"`, `response.type: "animation"`, tres fotogramas PNG llamados `1.png`, `2.png` y `3.png`, y `count` entre 1 y 10. Las respuestas textuales devuelven `intent: "text"`, `type: "text"` y `frames: []`; no inician animación.

## Validación

Desde `front-end`:

```powershell
npm run build
```
