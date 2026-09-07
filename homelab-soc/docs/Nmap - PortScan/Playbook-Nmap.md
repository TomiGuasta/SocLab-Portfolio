---
tipo: "Playbook"
categoria: "Reconnaissance"
estado: "Documentado"
fecha: 2026-09-07
táctica: "Reconnaissance"
técnica_asociada: "T1595.002"
---

# Playbook: Reconocimiento de Puertos (Nmap)

## 0. Resumen de Activo y Telemetría
*   **Servicio/Puerto:** Escaneo de superficie (TCP/UDP)
*   **Log Sources (SIEM):** `syslog`, `auditd`, logs de Firewall (`ufw.log`)
*   **Criticidad del Activo:** Media

## 1. Disparadores (Triggers)
*   **Alerta SIEM:** Actividad inusual de escaneo (umbral de paquetes superado).
*   **IoC detectado:** Múltiples conexiones a puertos distintos desde una sola IP en poco tiempo.
*   **Patrones de Comportamiento:** Intentos de fingerprinting de SO y versiones de servicios.

## 2. Análisis Inicial y Evidencia (Lab)
*   **Comandos de Ataque/Validación:**
    ```bash
    # Escaneo Rápido / Ruidoso (-T4)
    nmap -sS -sV -T4 192.168.0.28
    # Escaneo Evasivo / Lento (-T2)
    nmap -sS -sV -T2 192.168.0.28
    ```
*   **Query de Validación (SIEM):**
    ```spl
    index=main 
    | stats count by src_ip, dest_port
    | where count > 50
    ```
*   **Output Esperado (Logs/Terminal):**
    ```text
    PORT     STATE SERVICE VERSION
    22/tcp   open  ssh     OpenSSH 8.9p1
    80/tcp   open  http    Apache httpd
    3306/tcp open  mysql   MariaDB
    ```

## 3. Acciones de Respuesta
*   **Contención:** Bloqueo preventivo de IP en Firewall (iptables/ufw).
*   **Erradicación:** Minimizar superficie de ataque (cerrar puertos innecesarios), ocultar banners de servicios.
*   **Recuperación:** Monitorear actividad tras el escaneo.

## 4. Resultados Esperados (Validación)
*   Mapeo de puertos abiertos (22, 80, 3306), versiones de servicios y fingerprint del SO.

## 5. Threat Hunting (Post-Incidente)
*   Investigar si tras el escaneo hubo intentos de conexión a puertos específicos detectados.
*   Buscar patrones de ataque basados en las versiones de servicio descubiertas.

## 6. Referencias MITRE
*   Técnica: [T1595.002 - Vulnerability Scanning](https://attack.mitre.org/techniques/T1595/002/)
