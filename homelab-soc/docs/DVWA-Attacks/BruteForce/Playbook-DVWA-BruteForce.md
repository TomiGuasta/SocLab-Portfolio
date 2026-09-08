---
tipo: "Playbook"
categoria: "Web Security"
estado: "Documentado"
fecha: 2026-09-08
táctica: "Credential Access"
técnica_asociada: "T1110.001 - Brute Force: Password Guessing"
---

# Playbook: DVWA Brute Force

## 0. Resumen de Activo y Telemetría
*   **Servicio/Puerto:** HTTP/80
*   **Log Sources (SIEM):** Apache Access Logs, Autenticación Web.
*   **Criticidad del Activo:** Media (Laboratorio)

## 1. Disparadores (Triggers)
*   **Alerta SIEM:** Múltiples fallos de inicio de sesión desde una única IP en un periodo corto.
*   **IoC detectado:** IP de origen repetitiva, códigos de respuesta HTTP 200 (si tiene éxito) o 401 (si falla).
*   **Patrones de Comportamiento:** Alto volumen de peticiones `POST` al endpoint de login (`/dvwa/login.php`).

## 2. Análisis Inicial y Evidencia (Lab)
*   **Guía Técnica (Laboratorio):** Intentar adivinar credenciales mediante fuerza bruta en la página de login de DVWA con nivel de seguridad bajo/medio.
*   **Comandos de Ataque/Validación:**
    ```bash
    # Ejemplo usando Burp Suite Intruder o script simple de Python
    python3 brute_dvwa.py --url http://127.0.0.1/dvwa/login.php --user admin --wordlist passwords.txt
    ```
*   **Query de Validación (SIEM):**
    ```spl
    index=web_logs sourcetype=apache_access status=401 | stats count by clientip | where count > 10
    ```
*   **Output Esperado (Logs/Terminal):**
    ```text
    192.168.1.5 - - [08/Sep/2026:10:00:01] "POST /dvwa/login.php HTTP/1.1" 401 ...
    ```

## 3. Acciones de Respuesta
*   **Contención:** Bloquear IP de origen en el Firewall/WAF.
*   **Erradicación:** Implementar bloqueo de cuenta tras N intentos fallidos, añadir CAPTCHA.
*   **Recuperación:** Resetear contraseña de la cuenta comprometida si el ataque tuvo éxito.

## 4. Resultados Esperados (Validación)
*   Si el ataque es real/exitoso, verás: Gran cantidad de logs de error 401 seguidos de un 200 exitoso con la misma IP.

## 5. Threat Hunting (Post-Incidente)
*   Revisar si la IP ha intentado acceder a otros directorios (`/admin`, `/config`).
*   Verificar si hubo cambios en la configuración del sitio o en la base de datos tras el acceso exitoso.

## 6. Referencias MITRE
*   Técnica: [https://attack.mitre.org/techniques/T1110/001/](https://attack.mitre.org/techniques/T1110/001/)
