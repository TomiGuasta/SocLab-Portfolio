# Análisis Técnico Post-Incidente

## Resumen Ejecutivo

Se realizó una simulación controlada de denegación de servicio basada en tráfico HTTP concurrente contra un servicio Apache alojado en Metasploitable 2.

El ejercicio tuvo como objetivo generar evidencia observable desde una perspectiva defensiva, permitiendo analizar:

- comportamiento del servicio bajo carga
- telemetría generada durante el evento
- impacto operativo sobre el host
- oportunidades de detección orientadas a SOC / Blue Team

---

## Entorno de Laboratorio

Infraestructura utilizada:

**Atacante:**
- Kali Linux

**Objetivo:**
- Metasploitable 2

**Servicio analizado:**
- Apache HTTP Server
- TCP/80

**Entorno:**
- VirtualBox
- Red Host-Only aislada

---

## Validación Previa del Servicio

Antes de iniciar la simulación se verificó la disponibilidad del servicio HTTP sobre el puerto TCP/80.

Comando utilizado:

```bash
nmap -p 80 192.168.56.101
```

Resultado esperado:

```text
80/tcp open http
```

Objetivo:

Confirmar que el servicio Apache se encontraba activo, escuchando y accesible antes del inicio de la prueba.

---

## Ejecución de la Simulación

Se utilizó ApacheBench para generar tráfico HTTP concurrente.

Comando utilizado:

```bash
ab -n 10000 -c 50 http://192.168.56.101/
```

Configuración:

- **10000 requests HTTP totales**
- **50 conexiones concurrentes**

Objetivo:

Simular presión operativa / agotamiento básico de recursos sobre el servicio web Apache.

---

## Evidencia Recolectada

Durante la simulación se realizaron tareas de monitorización en tiempo real desde Metasploitable.

### Monitorización de Recursos

Comando utilizado:

```bash
top
```

Observaciones:

- actividad observable de procesos Apache
- utilización dinámica de CPU
- variaciones en carga del sistema

---

### Monitorización de Logs HTTP

Comando utilizado:

```bash
tail -f /var/log/apache2/access.log
```

Observaciones:

- incremento masivo de eventos HTTP
- timestamps asociados al ataque
- IP origen identificable
- User-Agent utilizado por ApacheBench

Ejemplo observado:

```text
192.168.56.1 - - [28/May/2026:12:46:09 -0400] "GET / HTTP/1.0" 200 891 "-" "ApacheBench/2.3"
```

Interpretación:

- **192.168.56.1** → host atacante (Kali)
- **GET /** → solicitud HTTP a la página principal
- **200** → respuesta exitosa del servidor
- **ApacheBench/2.3** → User-Agent identificando la herramienta utilizada

También se observaron conexiones internas del propio servicio Apache:

```text
127.0.0.1 - - [28/May/2026:12:46:11 -0400] "OPTIONS * HTTP/1.0" 200 - "-" "Apache/2.2.8 (Ubuntu) DAV/2 (internal dummy connection)"
```

Interpretación:

Actividad interna normal generada por Apache para gestión de workers y mantenimiento del servicio.

---

### Observabilidad de Conexiones TCP

Comando utilizado:

```bash
watch -n1 'netstat -ant | grep :80 | wc -l'
```

Objetivo:

Monitorizar dinámicamente conexiones TCP asociadas al puerto 80.

Observaciones:

Durante la ejecución del ataque se observó incremento del número de conexiones relacionadas con el servicio HTTP.

Esto permitió visualizar en tiempo real el comportamiento concurrente generado por ApacheBench.

---

## Indicadores Observados (IOC)

Durante la simulación se identificaron los siguientes patrones relevantes para detección SOC:

### IOC 1 — Alta Frecuencia HTTP

Múltiples requests generados desde una misma IP en una ventana temporal reducida.

---

### IOC 2 — Burst Activity

Patrón consistente de tráfico repetitivo hacia el mismo recurso HTTP.

---

### IOC 3 — Incremento de Logging

Elevada generación de eventos registrados en:

```text
/var/log/apache2/access.log
```

---

### IOC 4 — Variación Operativa del Servicio

Actividad observable en CPU, procesos Apache y conexiones TCP durante el período de carga.

---

## Impacto Potencial en Entornos Reales

En un entorno productivo este comportamiento podría derivar en:

- degradación del rendimiento del servicio
- incremento de latencia
- agotamiento de recursos (CPU / memoria)
- crecimiento acelerado de logs
- indisponibilidad parcial o total del servicio

---

## Posibles Oportunidades de Detección

Desde una perspectiva Blue Team / SOC podrían implementarse mecanismos como:

- monitoreo de request rate HTTP
- alertas por bursts de tráfico
- correlación de IPs origen
- análisis de patrones repetitivos
- monitoreo de conexiones concurrentes
- integración de logs con SIEM (Splunk / ELK)

---

## Aprendizajes y Conclusiones

El ejercicio permitió comprender:

- funcionamiento básico de escenarios HTTP DoS / Resource Exhaustion
- importancia de la observabilidad en tiempo real
- utilidad del análisis de logs Apache
- monitoreo de recursos y conexiones TCP
- enfoque defensivo orientado a detección y análisis SOC

La simulación fue realizada exclusivamente dentro de un laboratorio controlado con fines educativos y de práctica técnica.
