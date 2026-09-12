---
tags: [infraestructura, victima, ubuntu, apache, mariadb, dvwa]
fecha: 2026-08-31
hostname: ubuntu-server
ip: 192.168.0.28
interfaz: WiFi
parent: [[Setup.md]]
---

# 🖥️ Host Víctima: Ubuntu Server

## 📌 Información General
Servidor dedicado dentro de la red local que aloja las aplicaciones vulnerables y los servicios expuestos para simular escenarios reales de ataque.

* **SO:** Ubuntu Server
* **Dirección IP:** `192.168.0.28` (Conexión WiFi)
* **Rol:** Target / Víctima en el Homelab

---

## ⚙️ Servicios Configurados

| Servicio | Puerto / Protocolo | Ubicación / Configuración |
| :--- | :--- | :--- |
| **OpenSSH** | 22 / TCP | `/etc/ssh/sshd_config` (Monitoreado por auditd) |
| **Apache2** | 80 / TCP | Servidor Web (`/var/www/html/`) |
| **MariaDB / MySQL** | 3306 / TCP | BD DVWA (Usuario: `tomi`) |
| **DVWA** | HTTP (`/dvwa/`) | Damn Vulnerable Web Application |
| **Splunk UF** | Agente de Logs | Envía telemetría al SIEM (`192.168.0.X:9997`) |
| **Auditd** | Daemon del Kernel | Reglas personalizadas en `/etc/audit/rules.d/lab-soc.rules` |

---

## 📂 Rutas Clave de Logs Monitoreados

* **Apache Access:** `/var/log/apache2/access.log`
* **Apache Error:** `/var/log/apache2/error.log`
* **Autenticación (SSH/Sudo):** `/var/log/auth.log`
* **Eventos del Sistema:** `/var/log/syslog`
* **Auditoría de Kernel:** `/var/log/audit/audit.log`