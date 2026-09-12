---
tags: [infraestructura, auditd, hardening, linux, rules]
fecha: 2026-08-31
archivo: /etc/audit/rules.d/lab-soc.rules
parent: [[Setup.md]]
---

# 🛡️ Reglas de Auditoría Personalizadas (auditd)

## 📌 Objetivo
Capturar eventos críticos del sistema operativo a nivel de kernel en el servidor Ubuntu (`192.168.0.28`) que no son registrados por los logs estándar de syslog o Apache.

---

## 📄 Contenido del Archivo `/etc/audit/rules.d/lab-soc.rules`

```bash
# Eliminar todas las reglas previas
-D

# Definir tamaño del buffer
-b 8192

# 1. Monitoreo de modificación de archivos de autenticación y usuarios
-w /etc/passwd -p wa -k identity_changes
-w /etc/shadow -p wa -k identity_changes
-w /etc/group -p wa -k identity_changes
-w /etc/sudoers -p wa -k privilege_changes

# 2. Monitoreo de cambios en la configuración de SSH
-w /etc/ssh/sshd_config -p wa -k sshd_config_changes

# 3. Monitoreo de ejecución de comandos con privilegio (Sudo)
-a always,exit -F arch=b64 -S execve -F euid=0 -k elevated_commands