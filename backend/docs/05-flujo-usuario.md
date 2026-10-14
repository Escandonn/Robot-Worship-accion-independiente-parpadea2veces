# Flujo de Usuario - Backend WORSHIP Mascot Robot

## Descripción
Este documento muestra el proceso completo desde que el usuario abre la interfaz del robot hasta que el rostro aparece en pantalla, incluyendo estados de carga, éxito, error y reintento.

## Flujo de Usuario Completo

```mermaid
flowchart TD
    %% Estados del usuario
    A[Usuario abre la aplicación] --> B[Frontend inicializado]
    B --> C[Frontend solicita componentes faciales]
    C --> D{Backend responde}
    
    %% Camino de éxito
    D -->|Éxito (HTTP 200)| E[Frontend recibe componentes]
    E --> F[Frontend decodifica Base64]
    F --> G[Frontend renderiza componentes]
    G --> H[Rostros del robot visible]
    H --> I[Usuario interactúa con el robot]
    
    %% Caminos de error
    D -->|Error 404| J[Error: Componentes faltantes]
    J --> K[Mostrar mensaje de error]
    K --> L[Opción: Reintentar]
    L --> M{¿Reintentar?}
    M -->|Sí| C
    M -->|No| N[Continuar con funcionalidad limitada]
    
    D -->|Error 500| O[Error: Servidor interno]
    O --> P[Mostrar mensaje de error]
    P --> Q[Opción: Reintentar]
    Q --> R{¿Reintentar?}
    R -->|Sí| C
    R -->|No| N
    
    %% Estados de carga
    C --> S[Mostrar indicador de carga]
    S --> D
    
    %% Estilos
    classDef proceso fill:#E3F2FD,stroke:#1565C0,stroke-width:2px;
    classDef decision fill:#FFF3E0,stroke:#EF6C00,stroke-width:2px;
    classDef exito fill:#E8F5E9,stroke:#2E7D32,stroke-width:2px;
    classDef error fill:#FFEBEE,stroke:#C62828,stroke-width:2px;
    classDef carga fill:#F3E5F5,stroke:#6A1B9A,stroke-width:2px;
    
    class B,C,F,G,H,I,L,M,Q,R proceso
    class D decisión
    class E,F,G,H exito
    class J,K,L,M,O,P,Q,R error
    class S carga
```

## Detalle de Cada Estado

### 1. Usuario abre la aplicación
- El usuario lanza la interfaz web del WORSHIP Mascot Robot
- El frontend Astro + React comienza su proceso de inicialización

### 2. Frontend inicializado
- El frontend ha cargado todos sus recursos necesarios (JS, CSS, etc.)
- Está listo para hacer la primera solicitud al backend para obtener los componentes faciales

### 3. Frontend solicita componentes faciales
- El frontend envía una solicitud GET a `/api/v1/face/initial`
- Se muestra un indicador de carga mientras espera la respuesta

### 4. Backend responde
- El punto de decisión donde el backend puede responder con éxito o varios tipos de errores

### 5. Éxito (HTTP 200)
- El backend retorna correctamente los componentes faciales codificados en Base64
- El frontend procede a procesar estos datos

### 6. Frontend decodifica Base64
- Cada componente facial tiene su campo `data` decodificado de Base64 a binario
- Se crean objetos Blob o URLs de datos para usar en elementos `<img>`

### 7. Frontend renderiza componentes
- Las imágenes se posicionan correctamente para formar el rostro completo del robot
- Se aplica cualquier CSS necesario para el posicionamiento y tamaño

### 8. Rostro del robot visible
- El usuario puede ver el rostro completo del WORSHIP Mascot Robot
- El sistema está listo para interacciones adicionales

### 9. Usuario interactúa con el robot
- El usuario puede realizar acciones que desencadenen otros comportamientos
- (Este sería el punto donde entraría en juego el endpoint de parpadeo en futuras implementaciones)

### Estados de Error y Recuperación

#### Error 404: Componentes faltantes
- Indica que uno o más archivos PNG no se encontraron en la ubicación esperada
- Puede ocurrir durante el desarrollo o deployment si los assets no se copiaron correctamente
- El sistema ofrece la opción de reintentar (útil si el error es temporal)

#### Error 500: Servidor interno
- Indica un problema al leer los archivos de imagen (permisos, corrupción, etc.)
- O cualquier otro error inesperado en el procesamiento
- También ofrece opción de reintentar

#### Continuar con funcionalidad limitada
- Si el usuario decide no reintentar después de un error
- La aplicación podría mostrar una representación alternativa o simplificada
- O desactivar ciertas funcionalidades que dependan de los componentes faciales

## Consideraciones de Experiencia de Usuario

### Indicadores de Carga
- Durante la solicitud al backend, se muestra un spinner o mensaje de "Cargando rostro..."
- Mejora la percepción de rendimiento al proporcionar feedback visual

### Manejo de Errores Amigable
- Los mensajes de error están diseñados para ser comprensibles por usuarios no técnicos
- Se evitan detalles técnicos que puedan confundir o revelar información interna
- Se ofrecen acciones claras (reintentar) cuando es apropiado

### Reintentos Automáticos (Posible Mejora)
- En futuras versiones, podría implementarse un sistema de reintentos automáticos
- Con límite de intentos y backoff exponencial para evitar sobrecargar el servidor

### Feedback Visual de Error
- Además de mensajes textuales, se podrían usar íconos o colores para indicar estados
- Rojo para errores, amarillo para advertencias, verde para éxito

## Integración con Futuras Funcionalidades

Este flujo establece la base para interacciones más complejas:
1. El rostro inicial se muestra correctamente
2. El usuario puede solicitar acciones (como parpadear)
3. El frontend enviaría esas solicitudes al backend
4. El backend procesaría y retornaría instrucciones de animación
5. El frontend ejecutaría las animaciones solicitadas

El éxito de este flujo inicial es crítico para establecer la confianza del usuario en el sistema antes de introducir funcionalidades más avanzadas.