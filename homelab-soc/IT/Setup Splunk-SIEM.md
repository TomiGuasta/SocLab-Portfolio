---
tags: [infraestructura, siem, splunk, blue-team, telemetry]
fecha: 2026-08-31
componente: SIEM
hostname: splunk-server
ip_ejemplo: 192.168.1.5
rol: Centralización y Análisis de Telemetría
---

# 📊 SIEM: Splunk Enterprise

## 🌐 Contexto de Infraestructura (IaC Template)
Servidor SIEM configurado para la ingestión y análisis de telemetría proveniente de los endpoints del laboratorio.

* **Dirección IP:** `{{SIEM_IP}}` (Ejemplo: `192.168.1.5`)
* **Puerto Web UI:** `8000` (`http://{{SIEM_IP}}:8000`)
* **Puerto REST API:** `8089` (Utilizado para automatización y scripts)
* **Puerto Ingestion:** `9997` (Recepción desde Universal Forwarder)

## 🔌 Configuración de Ingestión
Se ha configurado el Add-on `Splunk_TA_nix` para normalizar los logs recibidos desde los endpoints Linux:

* **Fuerza Bruta (SSH/Sudo):** sourcetype `linux_secure` (`/var/log/auth.log`)
* **Web Exploitation (DVWA):** sourcetype `access_combined` (`/var/log/apache2/access.log`)
* **DoS Patterns:** sourcetype `apache_error` (`/var/log/apache2/error.log`)
* **Integridad (Kernel/Archivos):** sourcetype `auditd` (`/var/log/audit/audit.log`)

## 🛡️ Consideraciones de Seguridad (Defense Perspective)
* **Gestión de Credenciales:** NO almacenar credenciales en scripts de automatización. Utilizar `splunk.secret` o gestión de secretos del SO.
* **Control de Acceso:** Configurar autenticación robusta y limitar el acceso a la Web UI a la subred de gestión.
* **Licenciamiento:** Verificar que el volumen de ingestión diario no exceda los límites de la licencia para evitar interrupciones de servicio.