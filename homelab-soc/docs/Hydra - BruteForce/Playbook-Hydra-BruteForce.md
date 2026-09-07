---
tipo: "Playbook"
categoria: "Web Security"
estado: "Documentado"
fecha: 2026-09-07
táctica: "Credential Access"
técnica_asociada: "T1110.001"
---

# Playbook: Hydra - Brute Force

## 0. Resumen de Activo y Telemetría
*   **Servicio/Puerto:** SSH (22) / HTTP (80/443)
*   **Log Sources (SIEM):** `auth.log` (SSH), `access_log` (Web/DVWA)
*   **Criticidad del Activo:** Alta

## 1. Disparadores (Triggers)
*   **Alerta SIEM:** Múltiples fallos de autenticación seguidos de un éxito.
*   **IoC detectado:** IP origen haciendo múltiples peticiones POST/LOGIN con distintos usuarios.
*   **Patrones de Comportamiento:** Patrón "Fallo-Fallo-Éxito" o ráfaga de intentos fallidos en tiempo corto.

## 2. Análisis Inicial y Evidencia (Lab)
*   **Comandos de Ataque/Validación:**
    ```bash
    # Hydra Brute Force
    hydra -l admin -P passlist.txt ssh://192.168.0.28
    ```
*   **Query de Validación (SIEM):**
    ```spl
    index=main (sourcetype=auth OR sourcetype=access_combined)
    | stats count by src_ip, user, action
    | where count > 10
    ```
*   **Output Esperado (Logs/Terminal):**
    ```text
    [+] Target: 192.168.0.28
    [+] Password: password123
    [+] Authentication success
    ```

## 3. Acciones de Respuesta
*   **Contención:** Bloquear la IP atacante en Firewall (iptables/ufw).
*   **Erradicación:** Cambiar contraseñas comprometidas, forzar cierre de sesiones activas, habilitar MFA.
*   **Recuperación:** Validar acceso legítimo tras cambios de credenciales.

## 4. Resultados Esperados (Validación)
*   Mensajes de "Accepted password" en `auth.log` o "HTTP 200 OK" tras múltiples "401 Unauthorized" en Web.

## 5. Threat Hunting (Post-Incidente)
*   Buscar uso de credenciales comprometidas en otros servicios.
*   Revisar creación de nuevos usuarios o cambio de permisos (escalada de privilegios).

## 6. Referencias MITRE
*   Técnica: [T1110.001 - Brute Force: Password Guessing](https://attack.mitre.org/techniques/T1110/001/)
