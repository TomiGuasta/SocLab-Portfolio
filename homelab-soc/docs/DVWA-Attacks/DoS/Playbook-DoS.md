---
tipo: "Playbook"
categoria: "Network Security"
estado: "Documentado"
fecha: 2026-09-07
táctica: "Impact"
técnica_asociada: "T1498"
---

# Playbook: Denegación de Servicio (DoS)

## 0. Resumen de Activo y Telemetría
*   **Servicio/Puerto:** Apache2 / Puerto 80
*   **Log Sources (SIEM):** `apache_error`, `syslog`
*   **Criticidad del Activo:** Alta

## 1. Disparadores (Triggers)
*   **Alerta SIEM:** Error `mpm_prefork:error` (AH00161: server reached MaxRequestWorkers setting).
*   **IoC detectado:** Inundación de conexiones desde una IP única o conexiones persistentes incompletas.
*   **Patrones de Comportamiento:** Caída total del servicio web sin registros de finalización en `access.log`.

## 2. Análisis Inicial y Evidencia (Lab)
*   **Comandos de Ataque/Validación:**
    ```bash
    # Fase 1: Stress test
    ab -n 50000 -c 50 http://192.168.0.28/
    # Fase 2: Exhaustion
    slowloris 192.168.0.28 -p 80 -s 500
    ```
*   **Query de Validación (SIEM):**
    ```spl
    index=main sourcetype=apache_error 
    | search "MaxRequestWorkers" OR "server reached"
    | table _time, host, syslog_message
    ```
*   **Output Esperado (Logs/Terminal):**
    ```text
    [mpm_prefork:error] AH00161: server reached MaxRequestWorkers setting
    ```

## 3. Acciones de Respuesta
*   **Contención:** Bloquear IP atacante en Firewall (iptables/ufw), limitar conexiones por IP.
*   **Erradicación:** Implementar `mod_reqtimeout` y `mod_evasive`, ajustar `MaxRequestWorkers`.
*   **Recuperación:** Reiniciar servicio web (`sudo systemctl restart apache2`), monitorear logs.

## 4. Resultados Esperados (Validación)
*   Servidor web inaccesible, errores 507 en logs, o "No response".

## 5. Threat Hunting (Post-Incidente)
*   Verificar si el DoS fue una cortina de humo para otra actividad maliciosa.
*   Analizar logs de red anteriores al DoS en busca de escaneos de vulnerabilidades.

## 6. Referencias MITRE
*   Técnica: [T1498 - Network Denial of Service](https://attack.mitre.org/techniques/T1498/)
