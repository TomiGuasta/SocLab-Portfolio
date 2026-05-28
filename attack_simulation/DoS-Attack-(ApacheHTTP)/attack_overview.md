# Attack Overview

Se utilizó ApacheBench para generar tráfico HTTP concurrente contra el servicio web Apache.

Configuración utilizada:

- 10000 requests totales
- 50 conexiones concurrentes

Objetivo:

Simular presión operacional sobre el servicio HTTP y analizar el comportamiento observable desde la perspectiva de detección y monitoreo.

La simulación produjo:

- incremento masivo de requests HTTP
- crecimiento de eventos registrados en access.log
- aumento observable del trabajo del servicio Apache
