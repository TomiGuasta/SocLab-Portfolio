Proyecto de laboratorio orientado a Blue Team / SOC Analyst.

Se realizó una simulación controlada de agotamiento de recursos (HTTP Flood / DoS básico) contra un servicio Apache (puerto 80/tcp) alojado en Metasploitable 2.

El objetivo principal fue observar:

- comportamiento del servicio bajo carga
- generación de evidencia en tiempo real
- impacto operativo sobre recursos del host
- oportunidades de detección para workflows SOC

---

## Entorno utilizado

Atacante:

- Kali Linux

Objetivo:

- Metasploitable 2

Servicio atacado:

- Apache HTTP Server
- TCP/80

Infraestructura:

- VirtualBox
- Host-Only Network

---
