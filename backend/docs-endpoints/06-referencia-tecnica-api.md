# Referencia técnica de la API

## Base URL

En desarrollo local, la base URL predeterminada es `http://127.0.0.1:8000`.

## 1. Obtener componentes del rostro inicial

### Solicitud

| Propiedad | Valor |
|---|---|
| Método | `GET` |
| Ruta | `/api/v1/face/initial` |
| Cuerpo | Ninguno |
| Autenticación | No definida por este endpoint |

#### Ejemplo

```http
GET /api/v1/face/initial HTTP/1.1
Host: 127.0.0.1:8000
```

### Respuesta exitosa

**HTTP 200 OK**

```json
{
  "success": true,
  "components": [
    {
      "name": "boca",
      "type": "image/png",
      "data": "<BASE64_PNG>"
    },
    {
      "name": "nariz",
      "type": "image/png",
      "data": "<BASE64_PNG>"
    },
    {
      "name": "ojo-derecho",
      "type": "image/png",
      "data": "<BASE64_PNG>"
    },
    {
      "name": "ojo-izquierdo",
      "type": "image/png",
      "data": "<BASE64_PNG>"
    }
  ]
}
```

`data` contiene los bytes reales del PNG codificados en Base64. Las rutas y nombres de archivo se definen en `FaceRepository`.

### Errores

| HTTP | Causa | Detalle |
|---|---|---|
| 404 | Falta un archivo de componente | `One or more facial component files are missing` |
| 500 | Error de lectura | `Error reading facial component files` |
| 500 | Error inesperado | `An unexpected error occurred while processing facial components` |

## 2. Interpretar texto y determinar parpadeo

### Solicitud

| Propiedad | Valor |
|---|---|
| Método | `POST` |
| Ruta | `/api/v1/robot/interpret` |
| Tipo de contenido | `application/json` |
| Campo requerido | `text: string` |

#### Ejemplo

```http
POST /api/v1/robot/interpret HTTP/1.1
Host: 127.0.0.1:8000
Content-Type: application/json

{
  "text": "Haz dos parpadeos"
}
```

Groq recibe el texto junto con instrucciones para clasificar la intención. La respuesta debe ser un objeto JSON validable con `intent`, `content` y `count`. La clasificación no se basa en comprobar si el texto contiene una palabra clave.

Cada solicitud incluye en el mensaje de sistema la identidad permanente de WORSHIP como hechicero creado por Alejandro Escando, junto con la instrucción de no presentarse como bot o IA. La frase asociada al parpadeo es: «Cuando me pides que parpadee, tu vida no será la misma». Este contexto se aplica a todas las respuestas; el lema se usa en la respuesta cuando es pertinente, especialmente al confirmar una orden de parpadeo.

### Respuesta de animación

Para una orden afirmativa clasificada como `blink`, el backend devuelve HTTP 200:

```json
{
  "success": true,
  "intent": "blink",
  "response": {
    "type": "animation",
    "content": "Parpadeo detectado",
    "frames": [
      {
        "name": "1.png",
        "format": "png",
        "data": "<BASE64_PNG_1>"
      },
      {
        "name": "2.png",
        "format": "png",
        "data": "<BASE64_PNG_2>"
      },
      {
        "name": "3.png",
        "format": "png",
        "data": "<BASE64_PNG_3>"
      }
    ],
    "count": 2
  }
}
```

- `frames` contiene siempre los tres fotogramas existentes en el orden `1.png`, `2.png`, `3.png`.
- Cada `data` contiene los bytes del archivo correspondiente codificados en Base64.
- `count` representa los ciclos solicitados. El modelo acepta valores enteros entre 1 y 10; si no se especifica cantidad, Groq recibe instrucciones para devolver 1.
- Los marcadores `<BASE64_PNG_n>` son ilustrativos; la respuesta real contiene las cadenas Base64 de los archivos locales.

### Respuesta textual

Para una conversación, pregunta, negación o explicación clasificada como `text`, el backend responde HTTP 200:

```json
{
  "success": true,
  "intent": "text",
  "response": {
    "type": "text",
    "content": "¡Hola! Estoy listo para ayudarte.",
    "frames": []
  }
}
```

`content` procede de Groq. En esta rama no se leen ni codifican los PNG. El campo `count` se omite al serializar si su valor es `null`.

### Validaciones y errores

| HTTP | Causa | Comportamiento |
|---|---|---|
| 400 | `text` está vacío o solo contiene espacios | El servicio rechaza la entrada vacía. |
| 422 | Cuerpo JSON inválido o campo `text` ausente/no textual | Validación de solicitud de FastAPI/Pydantic. |
| 500 | Groq no está disponible, falla la llamada, la respuesta no valida o falla la lectura de un fotograma | El controlador devuelve un error general de procesamiento. |

La intención permitida es `blink` o `text`. El tipo de respuesta debe corresponder a la intención; el modelo también valida el orden y cantidad de fotogramas para animaciones, y que las respuestas de texto no contengan fotogramas ni ciclos.

## Archivos de imagen

- Rostro inicial: `app/assets/emociones/` según el catálogo de `FaceRepository`.
- Fotogramas de parpadeo: `app/assets/ojos/1.png`, `app/assets/ojos/2.png` y `app/assets/ojos/3.png`.
- Las rutas de fotogramas se resuelven desde la ubicación del módulo del repositorio, no dependen de una ruta absoluta específica del equipo.

## Configuración de Groq

El servicio carga `backend/.env` y usa:

```env
GROQ_API_KEY=tu_clave_de_groq
GROQ_MODEL=tu_modelo_disponible
```

Las variables de entorno definidas directamente en el proceso tienen prioridad sobre los valores de `.env`. No se debe incluir la clave en el frontend ni en documentación compartida.

## Ejecución y pruebas

Desde la carpeta `backend`:

```powershell
python -m uvicorn app.main:app --reload
```

La documentación interactiva de FastAPI está disponible en `http://127.0.0.1:8000/docs`.

Para probar ambos endpoints con la suite existente:

```powershell
python -m pytest -q tests/test_face_initial.py tests/test_robot_interpret.py
```
