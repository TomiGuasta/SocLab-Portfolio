---
tipo: "Tratamiento"
ataque: "Denegación de Servicio (DoS)"
herramienta: "Apache Stress/Slowloris"
fecha: 2026-09-24
estado: "Documentado"
---

# Tratamiento: Denegación de Servicio (DoS)

## 1. Definición del Riesgo
El ataque busca agotar los recursos del servidor web (CPU, RAM, conexiones concurrentes), impidiendo el acceso a los usuarios legítimos y provocando la caída del servicio.

## 2. Medidas de Mitigación (ISO 27002 / Controles)
*   **A.12.6.1 (Gestión de vulnerabilidades técnicas):** Configurar límites estrictos de recursos (`MaxRequestWorkers`) y timeouts (`mod_reqtimeout`).
*   **A.17.1.1 (Planificación de la continuidad de la seguridad):** Implementar estrategias de redundancia y alta disponibilidad.
*   **A.13.1.1 (Controles de red):** Utilizar WAF y Firewall para limitar la tasa de conexiones por IP (rate limiting).

## 3. Estrategia de Respuesta (Playbook Integrado)
*   **Detección:** Basado en `Playbook-DoS.md`, monitorizar `apache_error` buscando saturación de trabajadores o conexiones incompletas persistentes.
*   **Contención:** Bloqueo automático de IPs atacantes mediante `iptables/ufw` y ajuste dinámico de configuraciones de servidor.

## 4. Riesgo Residual
*   **Medio:** Aunque se mitiguen ataques DoS simples desde una sola IP, los ataques distribuidos (DDoS) son significativamente más difíciles de bloquear sin servicios especializados de mitigación en la nube.
