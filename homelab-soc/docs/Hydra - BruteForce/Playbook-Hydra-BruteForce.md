---
tipo: "Playbook"
categoria: "Network-Attacks"
estado: "Finalizado"
fecha: 2026-09-04
táctica: "Credential Access"
técnica_asociada: "T1110.001 - Password Guessing"
---

# Playbook: Fuerza Bruta SSH (Hydra)

## 0. Resumen de Activo
*   **Servicio/Puerto Atacado:** ==SSH / 22/TCP==

## 1. Disparadores (Triggers)
*   **Alerta SIEM:** Múltiples fallos de autenticación SSH (`Failed password`) desde una misma IP en un intervalo corto.
*   **IoC detectado:** Picos inusuales en `/var/log/auth.log` con patrón repetitivo de `Failed password`.
*   **Patrones de Comportamiento (Alta Fidelidad):**
    *   **AN1522 (Patrón crítico):** Fallos repetidos seguidos de éxito desde la misma IP.
    *   **AN1523:** Fallos de `sshd` con nombres de usuario repetidos.
    *   Correlación de intentos simultáneos contra múltiples cuentas desde la misma fuente.

## 2. Análisis Inicial (Investigación)
*   **Queries de validación (Splunk):**
    ```spl
    index=main sourcetype=linux_secure "Failed password"
    | stats count by src_ip, user
    | where count > 10
    ```
*   **Verificación de logs:**
    *   Revisar `grep "Failed password" /var/log/auth.log`.
    *   Validar protocolos adicionales (AN1525: SNMP, Telnet).
    *   Buscar eventos `Accepted password` tras fallos (AN1522).
*   **Contexto de Infraestructura:** Clasificado como **Password Guessing** (Iteración sobre usuario específico).
*   <details><summary><b>Otros puertos/servicios vulnerables a este ataque</b></summary>

    *   **RDP:** 3389/TCP | **SMB:** 445/TCP | **MSSQL:** 1433/TCP | **MySQL:** 3306/TCP | **LDAP:** 389/TCP | **SNMP:** 161/UDP
    </details>

## 3. Acciones de Respuesta
*   **Contención:** 
    *   Bloquear IP (firewall): `sudo ufw deny from <SRC_IP> to any port 22`.
    *   Terminar sesiones afectadas: `pkill -u <USER>`.
    *   **Alerta de Mitigación (M1036):** No implementar bloqueos demasiado estrictos que provoquen DoS auto-infligido.
*   **Erradicación:**
    *   Cambio de credenciales.
    *   Implementar SSH Keys + Deshabilitar `PasswordAuthentication` en `/etc/ssh/sshd_config`.
*   **Recuperación:**
    *   Verificar integridad.
    *   Reiniciar SSH: `sudo systemctl restart ssh`.

## 4. Inteligencia de Amenazas y Enriquecimiento Técnico
*   **Matriz MITRE:** [T1110.001 - Password Guessing](https://attack.mitre.org/techniques/T1110/001/)
*   **Actores/Herramientas:**
    *   *Herramientas:* **Hydra**, **CrackMapExec**, **Xbash**.
    *   *Actores:* **APT28**, **APT29**, **VOID MANTICORE**.
*   **Mitigaciones Operativas (MITRE):**
    *   **M1032:** Habilitación de MFA (obligatorio en servicios expuestos).
    *   **M1036:** Políticas de acceso condicional (bloqueo de proxies/VPNs).
    *   **M1051:** Actualización de software para forzar políticas de complejidad.
*   **Laboratorio/Writeup:** [[Attack/soc/docs/Network-Attacks/Hydra - BruteForce/SSH-BruteForce|Fuerza Bruta SSH contra Ubuntu Server]]
*   **Tooling/Scripts:** [[/]]
