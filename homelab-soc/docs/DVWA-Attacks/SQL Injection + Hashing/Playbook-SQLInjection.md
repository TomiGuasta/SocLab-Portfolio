---
tipo: "Playbook"
categoria: "Web Security"
estado: "Documentado"
fecha: 2026-09-09
táctica: "Initial Access / Execution"
técnica_asociada: "T1190 - Exploit Public-Facing Application"
---

# Playbook: SQL Injection

## 0. Resumen de Activo y Telemetría
*   **Servicio/Puerto:** Web App / DVWA
*   **Log Sources (SIEM):** `access.log`
*   **Criticidad del Activo:** Alta

## 1. Disparadores (Triggers)
*   **Alerta SIEM:** Detección de caracteres especiales (`'`, `"`, `--`, `UNION`, `SELECT`) en URLs de peticiones GET/POST.
*   **IoC detectado:** Peticiones HTTP conteniendo payload SQL.
*   **Patrones de Comportamiento:** Intento de bypass de autenticación o exfiltración de base de datos.

## 2. Análisis Inicial y Evidencia (Lab)
*   **Guía Técnica (Laboratorio):** [[Attack/soc/docs/Web-Security/SQL Injection + Hashing/SQL-Injection]]
*   **Comandos de Ataque/Validación:**
    ```text
    '1' OR '1'='1'
    ' UNION SELECT 1,2--
    ```
*   **Query de Validación (SIEM):**
    ```spl
    index=main sourcetype=access_combined uri="*UNION*SELECT*" OR uri="*OR*=*'"
    | table _time, clientip, method, uri, status
    ```
*   **Output Esperado (Logs/Terminal):**
    ```text
    Registros de acceso con parámetros inyectados.
    ```

## 3. Acciones de Respuesta
*   **Contención:** Bloqueo de la IP atacante, bloqueo del endpoint vulnerable temporalmente.
*   **Erradicación:** Implementar Prepared Statements (PDO), sanitizar entradas.
*   **Recuperación:** Auditoría de base de datos, rotación de credenciales comprometidas (especialmente si fueron crackeadas).

## 4. Resultados Esperados (Validación)
*   Si el ataque es exitoso, se observará la exfiltración de datos o el bypass de autenticación.

## 5. Threat Hunting (Post-Incidente)
*   Verificar si hubo exfiltración masiva de datos (dump de tablas).

## 6. Referencias MITRE
*   Técnica: [T1190](https://attack.mitre.org/techniques/T1190/)
