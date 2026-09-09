---
tipo: "Playbook"
categoria: "Web Security"
estado: "Documentado"
fecha: 2026-09-09
táctica: "Execution / Credential Access"
técnica_asociada: "T1059.007 - JavaScript"
---

# Playbook: Cross-Site Scripting (XSS)

## 0. Resumen de Activo y Telemetría
*   **Servicio/Puerto:** Web App / DVWA
*   **Log Sources (SIEM):** `access.log`
*   **Criticidad del Activo:** Media

## 1. Disparadores (Triggers)
*   **Alerta SIEM:** Peticiones conteniendo etiquetas script (`<script>`) o payloads XSS comunes.
*   **IoC detectado:** Payload XSS en parámetros de URL o campos de formularios.
*   **Patrones de Comportamiento:** Exfiltración de cookies o redirección maliciosa.

## 2. Análisis Inicial y Evidencia (Lab)
*   **Guía Técnica (Laboratorio):** [[Attack/soc/docs/Web-Security/XSS/Reflected-XSS]]
*   **Comandos de Ataque/Validación:**
    ```html
    <script>alert(document.cookie)</script>
    ```
*   **Query de Validación (SIEM):**
    ```spl
    index=main sourcetype=access_combined uri="*%3Cscript%3E*"
    | table _time, clientip, method, uri, status
    ```
*   **Output Esperado (Logs/Terminal):**
    ```text
    Peticiones HTTP con payloads codificados en la URL.
    ```

## 3. Acciones de Respuesta
*   **Contención:** Bloqueo de peticiones maliciosas (WAF), advertencia al usuario si aplica.
*   **Erradicación:** Sanitizar todas las entradas de usuario, implementar Content Security Policy (CSP), marcar cookies como `HttpOnly`.
*   **Recuperación:** Invalidación de sesiones comprometidas.

## 4. Resultados Esperados (Validación)
*   Ejecución de scripts en el navegador del usuario víctima, captura de cookies.

## 5. Threat Hunting (Post-Incidente)
*   Verificar accesos a la aplicación utilizando cookies exfiltradas.

## 6. Referencias MITRE
*   Técnica: [T1059.007](https://attack.mitre.org/techniques/T1059/007/)
