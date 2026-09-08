---
tipo: "Playbook"
categoria: "Web Security"
estado: "Documentado"
fecha: 2026-09-08
táctica: "Discovery"
técnica_asociada: "T1046 - Network Service Discovery / T1190 - Exploit Public-Facing Application"
---

# Playbook: DVWA Fuzzing

## 0. Resumen de Activo y Telemetría
*   **Servicio/Puerto:** HTTP/80
*   **Log Sources (SIEM):** Apache Access Logs
*   **Criticidad del Activo:** Media (Laboratorio)

## 1. Disparadores (Triggers)
*   **Alerta SIEM:** Alto número de peticiones a recursos inexistentes (HTTP 404) desde una única IP.
*   **IoC detectado:** IP de origen realizando peticiones secuenciales o aleatorias contra múltiples endpoints.
*   **Patrones de Comportamiento:** Peticiones rápidas intentando encontrar archivos o directorios ocultos (fuzzing).

## 2. Análisis Inicial y Evidencia (Lab)
*   **Guía Técnica (Laboratorio):** Utilizar herramientas de fuzzing para descubrir directorios o archivos ocultos en la aplicación web DVWA.
*   **Comandos de Ataque/Validación:**
    ```bash
    # Ejemplo usando ffuf
    ffuf -w /usr/share/wordlists/dirb/common.txt -u http://127.0.0.1/dvwa/FUZZ
    ```
*   **Query de Validación (SIEM):**
    ```spl
    index=web_logs sourcetype=apache_access status=404 | stats count by clientip | where count > 50
    ```
*   **Output Esperado (Logs/Terminal):**
    ```text
    192.168.1.5 - - [08/Sep/2026:10:05:01] "GET /dvwa/admin.php HTTP/1.1" 404 ...
    192.168.1.5 - - [08/Sep/2026:10:05:02] "GET /dvwa/config.php HTTP/1.1" 200 ...
    ```

## 3. Acciones de Respuesta
*   **Contención:** Bloquear IP de origen en el Firewall/WAF.
*   **Erradicación:** Asegurar que los archivos sensibles no sean accesibles públicamente, restringir acceso por directorio.
*   **Recuperación:** Auditar logs para ver qué recursos fueron descubiertos y asegurar su protección.

## 4. Resultados Esperados (Validación)
*   Si el ataque es real/exitoso, verás: Una alta tasa de errores 404 seguidos de intentos de acceso a recursos legítimos o restringidos.

## 5. Threat Hunting (Post-Incidente)
*   Identificar si el atacante tuvo éxito en acceder a archivos sensibles o de configuración tras el proceso de descubrimiento.
*   Buscar patrones similares de enumeración en otros directorios del servidor.

## 6. Referencias MITRE
*   Técnica: [https://attack.mitre.org/techniques/T1046/](https://attack.mitre.org/techniques/T1046/)
