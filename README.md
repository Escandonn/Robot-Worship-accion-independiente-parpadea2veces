# WORSHIP Mascot Robot
## README — Arquitectura de software y primera acción autónoma

**Proyecto:** WORSHIP Mascot Robot  
**Objetivo inicial:** implementar la primera acción autónoma del robot: parpadear dos veces.  
**Arquitectura:** Astro + React, Python + FastAPI y un módulo de control de comportamiento dirigido por IA.

---

## 1. Descripción del proyecto

La mascota robótica de WORSHIP es una plataforma de interacción que combina una representación visual animada, lógica de comportamiento y una arquitectura backend preparada para incorporar inteligencia artificial y controlar componentes físicos.

El objetivo es que el robot no se limite a mostrar animaciones predeterminadas, sino que pueda interpretar instrucciones, seleccionar comportamientos y ejecutar acciones de forma controlada.

La primera acción será el **parpadeo autónomo doble**, que permitirá validar el flujo entre la lógica de comportamiento, el backend y la representación visual.

## 2. Primera acción autónoma: doble parpadeo

La primera funcionalidad consiste en cerrar y abrir los ojos dos veces, ejecutando una secuencia visual definida.

**Comportamiento esperado:**

1. El sistema detecta o recibe una condición que activa el comportamiento.
2. El módulo de control selecciona la acción `blink_twice`.
3. El backend valida y envía la instrucción al frontend.
4. React ejecuta la animación correspondiente.
5. El robot recupera su estado visual normal.

La acción debe poder activarse mediante una instrucción de prueba y, posteriormente, mediante eventos autónomos definidos por el sistema.

## 3. Arquitectura tecnológica

### Frontend: Astro + React

Responsable de la interfaz y de la representación visual de la mascota.

Funciones:
- Mostrar el rostro y los ojos del robot.
- Ejecutar animaciones y transiciones.
- Gestionar estados visuales como reposo, parpadeo y expresiones.
- Recibir instrucciones del backend.
- Separar la lógica visual de la toma de decisiones.

### Backend: Python + FastAPI

Responsable de coordinar las acciones y comunicar los módulos del sistema.

Funciones:
- Exponer una API para recibir instrucciones.
- Validar las acciones solicitadas.
- Coordinar el módulo de comportamiento.
- Integrar el modelo de IA cuando corresponda.
- Entregar al frontend instrucciones estructuradas.
- Preparar la integración futura con MQTT y dispositivos físicos.

### Módulo de inteligencia artificial

Será responsable de interpretar el contexto y proponer la acción adecuada.

Por ejemplo, una entrada textual como «saluda al usuario» podría transformarse en una instrucción de comportamiento como `blink_twice` o, posteriormente, en una secuencia más compleja.

El modelo no debe modificar directamente la interfaz ni ejecutar código arbitrario. Su salida debe validarse mediante el backend antes de convertirse en una acción.

## 4. ¿Microservicios independientes o un solo servicio?

Para la primera versión se recomienda una **arquitectura modular dentro de un único backend FastAPI**.

Esto permite mantener responsabilidades separadas sin introducir la complejidad de desplegar y comunicar múltiples servicios desde el inicio.

| Componente | Responsabilidad | Despliegue inicial |
|---|---|---|
| Astro + React | Interfaz y animaciones | Frontend independiente |
| API FastAPI | Recepción y coordinación de acciones | Backend único |
| Módulo de comportamiento | Selección y validación de acciones | Módulo Python |
| Adaptador de IA | Interpretación del texto y propuesta de acciones | Módulo Python |
| Adaptador MQTT | Comunicación con hardware físico | Integración futura |

**Importante:** separar módulos no significa que sean microservicios. Un microservicio tiene su propio proceso de ejecución y despliegue, y se comunica con otros componentes mediante interfaces definidas.

La separación física del modelo de IA solo será necesaria si sus requisitos de cómputo, escalabilidad, seguridad o mantenimiento lo justifican.

## 5. Flujo de ejecución

El flujo inicial será:

1. Se recibe un texto o evento.
2. El backend determina la acción permitida, con apoyo del modelo de IA cuando sea necesario.
3. El módulo de comportamiento genera una instrucción estructurada.
4. FastAPI devuelve la instrucción al frontend.
5. React reproduce la animación.
6. El sistema puede registrar el resultado para diagnóstico.

Ejemplo de instrucción:

```json
{
  "action": "blink_twice",
  "target": "eyes",
  "parameters": {
    "count": 2,
    "duration_ms": 250
  }
}
```

Esta instrucción representa el contrato de comunicación entre backend y frontend. El tiempo indicado es una configuración inicial de referencia, no una duración obligatoria.

## 6. API inicial

### `POST /robot/action`

Solicita la ejecución de una acción visual permitida.

Ejemplo de solicitud:

```json
{
  "action": "blink_twice"
}
```

Ejemplo de respuesta:

```json
{
  "accepted": true,
  "action": "blink_twice",
  "target": "eyes",
  "parameters": {
    "count": 2,
    "duration_ms": 250
  }
}
```

La respuesta confirma que la acción fue aceptada por el backend; no implica que la animación ya haya terminado.

En esta primera versión, el frontend puede ejecutar la animación a partir de la respuesta HTTP. Si posteriormente se necesitan eventos continuos, estados en tiempo real o múltiples clientes, se podrá incorporar WebSocket o un mecanismo de mensajería apropiado.

## 7. Estructura de carpetas propuesta

```text
worship-mascot-robot/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── RobotFace.tsx
│   │   ├── animations/
│   │   │   └── blink.ts
│   │   ├── services/
│   │   │   └── robotApi.ts
│   │   └── pages/
│   └── package.json
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   │   └── robot.py
│   │   ├── services/
│   │   │   ├── behavior_service.py
│   │   │   └── ai_service.py
│   │   ├── schemas/
│   │   │   └── robot_action.py
│   │   └── adapters/
│   │       └── mqtt_adapter.py
│   └── requirements.txt
│
└── README.md
```

Esta estructura es una propuesta inicial. Los directorios de IA y MQTT pueden comenzar como módulos preparados para integración, sin necesidad de implementarlos por completo en la primera iteración.

## 8. Seguridad y control de acciones

El modelo de IA no debe tener acceso irrestricto al hardware.

Todas las acciones deben pasar por una lista de comportamientos permitidos y por la validación del backend. Los parámetros, los tiempos y los objetivos de cada acción deben tener límites definidos.

Para las primeras pruebas, el doble parpadeo será una acción visual sin efectos físicos. Cuando se incorpore hardware real, el backend deberá controlar los permisos, los estados y las condiciones de ejecución.

## 9. Plan de desarrollo

- [ ] Crear el frontend Astro + React.
- [ ] Implementar el componente visual del rostro.
- [ ] Desarrollar la animación de doble parpadeo.
- [ ] Crear la API FastAPI para solicitar acciones.
- [ ] Definir el contrato JSON entre frontend y backend.
- [ ] Implementar el módulo de comportamiento.
- [ ] Integrar el modelo de IA para seleccionar acciones a partir del texto.
- [ ] Validar la ejecución y gestionar errores.
- [ ] Preparar la comunicación MQTT para futuras interacciones con hardware.
- [ ] Evaluar la separación en microservicios cuando existan necesidades reales.

## 10. Resultado esperado

La primera versión de WORSHIP Mascot Robot demostrará que una acción puede seleccionarse desde el backend, representarse mediante una instrucción estructurada y ejecutarse visualmente en el frontend.

El doble parpadeo será la base para ampliar el sistema con nuevas expresiones, movimientos, respuestas contextuales y, posteriormente, comportamientos coordinados con componentes físicos.

**Principio de diseño:** la IA decide o propone el comportamiento, el backend valida y coordina, y el frontend representa la acción. Cada responsabilidad debe evolucionar sin acoplar innecesariamente los componentes.