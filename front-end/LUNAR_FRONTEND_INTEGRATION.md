# Integración del logotipo lunar en el frontend

El endpoint `GET /api/v1/face/initial` incluye el logotipo `lunar` junto con
los componentes del rostro. El frontend debe mostrarlo como una imagen estática
centrada en la frente. No es un ojo ni forma parte de la animación de parpadeo.

## Contrato de la API

La respuesta mantiene la estructura habitual:

```json
{
  "success": true,
  "components": [
    {
      "name": "lunar",
      "type": "image/png",
      "data": "<PNG codificado en Base64>"
    }
  ]
}
```

El arreglo también contiene `boca`, `nariz`, `ojo-derecho` y
`ojo-izquierdo`. El ejemplo muestra solo el objeto nuevo. No se requiere una
solicitud adicional: `fetchFaceInitial()` recibe los cinco componentes.

## Renderizado y posición

El componente debe buscarse por el nombre `lunar`, y su `src` se construye con
el tipo MIME y los datos Base64:

```tsx
const lunar = components.find((component) => component.name === "lunar");

{lunar && (
  <img
    src={`data:${lunar.type};base64,${lunar.data}`}
    alt=""
    aria-hidden="true"
    style={buildStyle("lunar")}
  />
)}
```

La posición se configura en `src/config/faceLayout.ts`, en porcentajes del
contenedor del rostro:

```ts
lunar: {
  x: 38,
  y: 6,
  width: 24,
  height: 12,
},
```

`x: 38` y `width: 24` centran horizontalmente la imagen. `y: 6` la coloca en
la parte central-superior de la frente, sin pegarla al borde superior. Estos
valores son un punto de partida visual: se pueden ajustar `y`, `width` y
`height` según la composición final del rostro y el tamaño de pantalla. La
imagen fuente mide 696 × 359 px; conserva una proporción aproximada de 1.94:1
al ajustar su tamaño.

## Independencia del parpadeo

- El logotipo se obtiene del componente `lunar` y se renderiza siempre que el
  endpoint inicial lo devuelva.
- Los fotogramas de parpadeo sustituyen temporalmente la imagen de los ojos,
  no la del logotipo.
- No debe usarse `eyeClassName` ni añadirse el logotipo a la lista de
  fotogramas.
- El estilo `face-lunar` aplica una sombra dorada sutil, sin la animación ni
  los efectos reservados para los ojos.

## Archivos de referencia

- `src/services/faceService.ts`: valida que la respuesta inicial incluya los
  cinco componentes.
- `src/components/FaceRenderer.tsx`: renderiza el logotipo como una capa
  independiente.
- `src/config/faceLayout.ts`: controla su ubicación y tamaño.
- `src/styles/face.css`: contiene su estilo visual.
