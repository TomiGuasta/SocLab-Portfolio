---
tags: [infraestructura, victima, ubuntu, apache, mariadb, dvwa]
fecha: 2026-08-31
componente: Host Víctima
hostname: ubuntu-server
ip_ejemplo: 192.168.1.20
rol: Target / Víctima en el Homelab
---

# 🖥️ Host Víctima: Ubuntu Server

## 🌐 Contexto de Infraestructura (IaC Template)
Servidor dedicado dentro de la red del laboratorio que aloja aplicaciones vulnerables y servicios expuestos para la simulación de escenarios de ataque.

* **SO:** Ubuntu Server
* **Dirección IP:** `{{TARGET_IP}}` (Ejemplo: `192.168.1.20`)

## ⚙️ Servicios Configurados
| Servicio | Puerto / Protocolo | Configuración / Ruta |
| :--- | :--- | :--- |
| **OpenSSH** | 22 / TCP | `/etc/ssh/sshd_config` (Auditado) |
| **Apache2** | 80 / TCP | Servidor Web (`/var/www/html/`) |
| **MariaDB / MySQL** | 3306 / TCP | BD DVWA |
| **DVWA** | HTTP (`/dvwa/`) | Damn Vulnerable Web Application |
| **Splunk UF** | Agente de Logs | Envía telemetría al SIEM (`{{SIEM_IP}}:9997`) |
| **Auditd** | Kernel Daemon | `/etc/audit/rules.d/lab-soc.rules` |

## 📂 Telemetría y Monitoreo (Logs)
Los siguientes logs son ingeridos por el SIEM para el análisis:
* **Apache Access/Error:** `/var/log/apache2/`
* **Autenticación (SSH/Sudo):** `/var/log/auth.log`
* **Eventos del Sistema:** `/var/log/syslog`
* **Auditoría de Kernel:** `/var/log/audit/audit.log`

## 🛡️ Consideraciones de Seguridad (Defense Perspective)
* **Principio de Mínimo Privilegio:** Las aplicaciones web (como DVWA) deben ejecutarse con un usuario limitado (ej: `www-data`), nunca con `root`.
* **Hardening:** Aplicar reglas de `iptables` o `ufw` para limitar el acceso a la interfaz de administración y base de datos a IPs autorizadas.
* **Integridad:** La configuración de `auditd` es vital para detectar intentos de escalada de privilegios (`T1068`).