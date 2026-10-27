# Integración del frontend con WORSHIP Face Detection API

Guía para conectar el frontend existente con la API: el usuario selecciona una
imagen, el frontend la envía al backend, recibe el PNG anotado y lo muestra.
No requiere reconstruir la interfaz; la imagen se envía al backend configurado.

## Datos de la API

| Dato | Valor |
|---|---|
| URL base desplegada | `https://backend-tau-seven-48jsbet9kg.vercel.app` |
| Documentación interactiva | <https://backend-tau-seven-48jsbet9kg.vercel.app/docs> |
| Esquema OpenAPI | <https://backend-tau-seven-48jsbet9kg.vercel.app/openapi.json> |
| Salud de la API | `GET https://backend-tau-seven-48jsbet9kg.vercel.app/health` |
| Validar si hay rostro | `POST /api/v1/face/validate` |
| Recibir imagen anotada | `POST /api/v1/face/annotate` |

Las URLs completas de los endpoints principales son:

- Validación: <https://backend-tau-seven-48jsbet9kg.vercel.app/api/v1/face/validate>
- Anotación: <https://backend-tau-seven-48jsbet9kg.vercel.app/api/v1/face/annotate>

Los endpoints de rostro son `POST`: no se prueban pegando su URL en la barra
del navegador. La imagen se envía en el cuerpo de la solicitud.

## Contrato de la solicitud

| Parámetro | Valor requerido | Descripción |
|---|---|---|
| Método | `POST` | Ambos endpoints |
| Cuerpo | `multipart/form-data` | No enviar JSON ni Base64 |
| Campo del archivo | `file` | Debe contener exactamente un archivo |
| Formatos admitidos | JPEG, PNG y WebP | Deben coincidir el formato y el tipo MIME |
| Tamaño máximo | 5 MiB por defecto | `5 * 1024 * 1024` bytes; el backend puede configurarlo |
| Parámetros de URL | Ninguno | No se necesitan query params ni autorización |

El navegador crea el `Content-Type` multipart con su `boundary`. **No establezcas
manualmente el header `Content-Type`** al usar `FormData`.

## Flujo recomendado de la interfaz

1. Permitir que el usuario seleccione un archivo de imagen.
2. Validar en el cliente que el tipo sea JPEG, PNG o WebP y que pese como máximo
   5 MiB. Esta validación mejora la experiencia; el backend vuelve a validar.
3. Mostrar la vista previa original si la interfaz ya la contempla.
4. Al enviar, desactivar el botón y mostrar un estado de carga.
5. Enviar el archivo a `/api/v1/face/annotate`.
6. Si la respuesta es exitosa, leer el cuerpo como `Blob` y mostrarlo en un
   `<img>`. La respuesta es un PNG, no JSON.
7. Si la respuesta no es exitosa, leer el JSON de error y mostrar un mensaje
   útil. No intentar mostrar ese JSON como imagen.
8. Permitir volver a seleccionar o procesar otra imagen y liberar las URLs de
   vista previa creadas con `URL.createObjectURL`.

El endpoint `/api/v1/face/validate` es opcional: úsalo si la interfaz necesita
informar primero el resultado de detección. La anotación ya detecta el rostro y
devuelve `404` cuando no encuentra ninguno, por lo que un flujo que solo muestra
la imagen anotada puede llamar directamente a `/annotate`.

## Ejemplo TypeScript independiente del framework

```ts
const API_BASE_URL =
  "https://backend-tau-seven-48jsbet9kg.vercel.app";
const MAX_FILE_SIZE = 5 * 1024 * 1024;
const ACCEPTED_TYPES = ["image/jpeg", "image/png", "image/webp"];

type ApiError = {
  success: false;
  error: {
    code: string;
    message: string;
  };
};

function validateImageFile(file: File): void {
  if (!ACCEPTED_TYPES.includes(file.type)) {
    throw new Error("Selecciona una imagen JPEG, PNG o WebP.");
  }

  if (file.size === 0) {
    throw new Error("El archivo está vacío.");
  }

  if (file.size > MAX_FILE_SIZE) {
    throw new Error("La imagen no debe superar los 5 MiB.");
  }
}

async function readApiError(response: Response): Promise<ApiError | null> {
  try {
    return (await response.json()) as ApiError;
  } catch {
    return null;
  }
}

export async function annotateImage(file: File): Promise<Blob> {
  validateImageFile(file);

  const formData = new FormData();
  formData.append("file", file);

  let response: Response;
  try {
    response = await fetch(`${API_BASE_URL}/api/v1/face/annotate`, {
      method: "POST",
      body: formData,
    });
  } catch {
    throw new Error(
      "No se pudo conectar con la API. Comprueba la conexión y la configuración CORS."
    );
  }

  if (!response.ok) {
    const body = await readApiError(response);
    throw new Error(
      body?.error?.message ?? `La API respondió con el estado ${response.status}.`
    );
  }

  const contentType = response.headers.get("content-type") ?? "";
  if (!contentType.toLowerCase().includes("image/png")) {
    throw new Error("La API respondió, pero no devolvió una imagen PNG.");
  }

  return response.blob();
}
```

`readApiError` tolera respuestas no JSON —por ejemplo, un error del proxy— para
que el frontend pueda mostrar un mensaje genérico en vez de fallar al procesar
el error. Si se prefiere no capturar fallos de lectura JSON, se puede cambiar
esta función según las convenciones del proyecto.

### Uso desde un componente

El siguiente ejemplo muestra la lógica central. Integra los estados en el
componente y el sistema de notificaciones que ya utiliza el frontend:

```tsx
const [selectedFile, setSelectedFile] = useState<File | null>(null);
const [isLoading, setIsLoading] = useState(false);
const [error, setError] = useState<string | null>(null);
const [resultUrl, setResultUrl] = useState<string | null>(null);

useEffect(() => {
  if (!resultUrl) return;
  return () => URL.revokeObjectURL(resultUrl);
}, [resultUrl]);

async function handleImage(file: File) {
  setIsLoading(true);
  setError(null);
  setSelectedFile(file);
  setResultUrl(null);

  try {
    const annotatedBlob = await annotateImage(file);
    setResultUrl(URL.createObjectURL(annotatedBlob));
  } catch (caught) {
    setError(
      caught instanceof Error ? caught.message : "No se pudo procesar la imagen."
    );
  } finally {
    setIsLoading(false);
  }
}
```

Por ejemplo, conecta `handleImage` al envío del formulario usando el archivo
seleccionado (`selectedFile`) y desactiva el botón mientras `isLoading` sea
`true`.

Renderiza la imagen resultante cuando `resultUrl` tenga valor:

```tsx
{resultUrl && (
  <img src={resultUrl} alt="Imagen con el logotipo WORSHIP sobre el rostro" />
)}
```

El `useEffect` de limpieza del ejemplo libera la URL anterior al cambiar
`resultUrl` y al desmontar el componente, después de que React actualiza la
vista.

## Respuesta de cada endpoint

### `POST /api/v1/face/annotate`

- Éxito con rostro: `200 OK`, `Content-Type: image/png`, cuerpo binario PNG.
  Convierte la respuesta con `response.blob()` y úsala como `src` de un `<img>`.
- Sin rostro: `404 Not Found`, JSON:

  ```json
  {
    "success": false,
    "error": {
      "code": "FACE_NOT_DETECTED",
      "message": "No se detectó un rostro; no se generó ninguna imagen."
    }
  }
  ```

- La imagen de salida conserva la imagen enviada y añade el logotipo `WORSHIP`
  rojo en la zona estimada de la frente de cada rostro detectado.

### `POST /api/v1/face/validate` (opcional)

- `200 OK`, `Content-Type: application/json`:

  ```json
  {
    "success": true,
    "is_face": true,
    "faces_count": 1,
    "message": "Se detectó al menos un rostro."
  }
  ```

- Si la imagen es válida y no encuentra rostros, devuelve igualmente `200 OK`,
  con `is_face: false`, `faces_count: 0` y el mensaje
  `"No se detectaron rostros."`.
- Este endpoint solo informa el resultado; no devuelve la imagen anotada.

## Errores que debe manejar el frontend

Los errores de la API siguen este formato JSON:

```json
{
  "success": false,
  "error": {
    "code": "INVALID_IMAGE",
    "message": "El archivo no contiene una imagen válida."
  }
}
```

| Estado | Código habitual | Causa | Acción sugerida |
|---|---|---|---|
| `400` | `EMPTY_FILE`, `INVALID_IMAGE` o `INVALID_FILE_COUNT` | Archivo vacío, contenido inválido o cantidad de archivos distinta de uno | Pedir seleccionar una sola imagen válida |
| `404` | `FACE_NOT_DETECTED` | La anotación no encontró rostros | Informar que no se detectó un rostro y permitir elegir otra imagen |
| `413` | `FILE_TOO_LARGE` | Se superó el límite de carga | Pedir una imagen de hasta 5 MiB |
| `415` | `UNSUPPORTED_MEDIA_TYPE` | Tipo no admitido | Aceptar JPEG, PNG o WebP |
| `422` | `MISSING_FILE` o `INVALID_REQUEST` | Falta el campo `file` o la solicitud no es válida | Comprobar que se añadió el archivo a `FormData` como `file` |
| Error de red | No hay respuesta HTTP | Sin conexión o proxy/API no disponible | Mostrar un aviso de conexión y revisar el proxy y el despliegue |

El texto de `error.message` puede mostrarse directamente al usuario. Utiliza el
código HTTP y/o `error.code` para decidir el flujo; no asumas que todos los
errores tienen el mismo formato si interviene un proxy o una plataforma de
despliegue.

## Proxy para desarrollo local y Vercel

El frontend envía la imagen a la ruta del mismo origen
`/api/v1/face/annotate`, evitando solicitudes directas del navegador al dominio
de la API y su bloqueo CORS. La configuración ya incluida reenvía esa ruta:

- En desarrollo (`npm run dev`) y previsualización local (`npm run preview`),
  `astro.config.mjs` proxifica la ruta al backend.
- En Vercel, `vercel.json` reescribe la misma ruta al backend. Asegúrate de que
  el proyecto de Vercel tenga como **Root Directory** `front-end` para que se
  aplique este archivo.

La configuración local apunta al backend desplegado documentado en esta guía.
Si quieres usar un backend local, cambia `target` en `astro.config.mjs` a
`http://127.0.0.1:8000`; la reescritura de Vercel seguirá apuntando al backend
desplegado.

No se requiere configurar CORS en el backend mientras las solicitudes pasen
por estos proxies del mismo origen. La base `PUBLIC_API_BASE_URL` existente se
conserva para el chat y otros endpoints; no se necesitan secretos ni tokens.

## Consideraciones de privacidad y UX

- El endpoint procesa la imagen en memoria y no la guarda como archivo de
  aplicación; informa al usuario que la imagen se enviará al backend para su
  procesamiento.
- El detector puede no encontrar rostros de perfil, pequeños, ocultos,
  inclinados o con mala iluminación. No presentes el resultado como una
  identificación de la persona.
- Mantén la imagen original disponible para permitir reintentar o descargarla
  según las funciones que ya tenga la interfaz.
- Para descargas, asigna la URL temporal a un enlace con `download` en vez de
  convertir el PNG a Base64.
- Revoca las URLs creadas con `URL.createObjectURL` cuando dejen de usarse.

## Prueba rápida con curl

Desde una terminal, sustituye la ruta por una imagen local:

```powershell
curl.exe -X POST "https://backend-tau-seven-48jsbet9kg.vercel.app/api/v1/face/annotate" `
  -F "file=@C:\ruta\a\rostro.jpg" `
  --output rostro-anotado.png
```

Si la API devuelve `404`, revisa el JSON de error: significa que no detectó un
rostro y no hay un PNG que mostrar.
