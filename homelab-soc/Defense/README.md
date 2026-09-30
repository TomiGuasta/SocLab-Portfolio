---
tags: [siem, splunk, alerts, savedsearches, blue-team, detection]
fecha: 2026-09-30
componente: Splunk SIEM - Automation & Detection
---

# 🚨 Automatización de Alertas en Splunk (`savedsearches.conf`)

Este directorio contiene la configuración de búsquedas guardadas y alertas automatizadas (`savedsearches.conf`) traducidas directamente desde los playbooks operativos del portafolio (`Defense/01_Playbooks/`).

## 📁 Estructura
- `savedsearches.conf`: Archivo de configuración nativo de Splunk con las alertas preconfiguradas para detección de amenazas en el Home Lab.

## ⚙️ Reglas de Detección Incluidas

1. **SSH Brute Force (`ssh_brute_force_detection`)**
   - **Severidad:** Media (3)
   - **Frecuencia:** Cada 5 minutos.
   - **SPL:** `index=main (sourcetype=linux_secure OR sourcetype=auth) "Failed password" | stats count by src_ip, user | where count >= 5`

2. **DVWA Web Brute Force (`dvwa_brute_force_detection`)**
   - **Severidad:** Media (3)
   - **Frecuencia:** Cada 5 minutos.
   - **SPL:** `index=main sourcetype=access_combined status=401 | stats count by clientip, uri | where count > 10`

3. **GoBuster / Fuzzing Directory Scanning (`gobuster_fuzzing_detection`)**
   - **Severidad:** Baja/Media (2)
   - **Frecuencia:** Cada 5 minutos.
   - **SPL:** `index=main sourcetype=access_combined (status=404 OR status=403) | stats count by clientip | where count > 50`

4. **SQL Injection (`sql_injection_detection`)**
   - **Severidad:** Alta (4)
   - **Frecuencia:** Cada 1 minuto.
   - **SPL:** `index=main sourcetype=access_combined (uri="*UNION*SELECT*" OR uri="*OR*=*'") | stats count by clientip, uri`

5. **Cross-Site Scripting XSS (`xss_attack_detection`)**
   - **Severidad:** Media (3)
   - **Frecuencia:** Cada 1 minuto.
   - **SPL:** `index=main sourcetype=access_combined (uri="*%3Cscript%3E*") | stats count by clientip, uri`

6. **Auditd Critical File Modification (`auditd_sensitive_file_modification`)**
   - **Severidad:** Crítica (5)
   - **Frecuencia:** Cada 5 minutos.
   - **SPL:** `index=main (key=passwd_changes OR key=shadow_changes OR key=sudoers_changes) | table _time, host, exe, uid, success, key`

---

## 🛠️ Instrucciones de Despliegue en Splunk

Para desplegar estas alertas en tu instancia de Splunk Enterprise:

1. Ubicar el archivo de configuración en la app de búsqueda (por defecto `search`):
   ```bash
   /opt/splunk/etc/apps/search/local/savedsearches.conf
   ```
   *(Si el archivo ya existe, puedes fusionar las secciones correspondientes).*

2. Reiniciar el servicio de Splunk o recargar la configuración de la aplicación:
   ```bash
   /opt/splunk/bin/splunk restart
   ```
   o vía REST / Web UI: `http://<splunk-ip>:8000/en-US/debug/refresh`
