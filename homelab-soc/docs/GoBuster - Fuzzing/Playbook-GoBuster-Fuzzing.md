---
tipo: "Playbook"
categoria: "Web Security"
estado: "Documentado"
fecha: 2026-09-09
táctica: "Reconocimiento"
técnica_asociada: "T1595.003 - Active Scanning: Wordlist Scanning"
---

# Playbook: GoBuster Fuzzing

## 0. Resumen de Activo y Telemetría
*   **Servicio/Puerto:** Puerto 80 / Apache2
*   **Log Sources (SIEM):** `access.log`, `error.log`
*   **Criticidad del Activo:** Media

## 1. Disparadores (Triggers)
*   **Alerta SIEM:** Aumento inusual de peticiones 404 para un mismo cliente.
*   **IoC detectado:** Peticiones rápidas a múltiples directorios/archivos desde una IP, gran cantidad de respuestas 404 seguidas de 200.
*   **Patrones de Comportamiento:** Escaneo de directorios con herramientas como GoBuster, Dirb o Ffuf.

## 2. Análisis Inicial y Evidencia (Lab)
*   **Guía Técnica (Laboratorio):** [[Attack/soc/docs/Web-Security/GoBuster - Fuzzing/Readme]]
*   **Comandos de Ataque/Validación:**
    ```bash
    gobuster dir -u http://<IP_UBUNTU> -w /usr/share/wordlists/dirb/common.txt
    ```
*   **Query de Validación (SIEM):**
    ```spl
    index=main sourcetype=access_combined status!=404 clientip=<IP_ATACANTE>
    | table _time, clientip, method, uri, status
    | sort _time
    ```
*   **Output Esperado (Logs/Terminal):**
    ```text
    Status: 200, URL: /admin
    Status: 200, URL: /backup
    ```

## 3. Acciones de Respuesta
*   **Contención:** Bloqueo de la IP atacante mediante firewall (`ufw` o `iptables`).
*   **Erradicación:** Revisar directorios expuestos y ajustar permisos o eliminar archivos innecesarios.
*   **Recuperación:** Validar acceso normal al servicio.

## 4. Resultados Esperados (Validación)
*   Si el escaneo es exitoso, verás una lista de directorios encontrados en la consola del atacante y múltiples registros en los logs del servidor.

## 5. Threat Hunting (Post-Incidente)
*   Revisar si los directorios encontrados fueron accedidos posteriormente para exfiltrar información.

## 6. Referencias MITRE
*   Técnica: [T1595.003](https://attack.mitre.org/techniques/T1595/003/)
