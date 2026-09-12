---
tags: [infraestructura, siem, splunk, blue-team, telemetry]
fecha: 2026-08-31
hostname: windows-host
ip: 192.168.0.X
licencia: Splunk Free
parent: [[Setup.md]]
---

# 📊 SIEM: Splunk Enterprise

## 📌 Información General
Servidor SIEM alojado en el host principal de desarrollo. Ingiere y centraliza la telemetría enviada en tiempo real por el *Splunk Universal Forwarder* instalado en el Ubuntu Server.

* **SO Host:** Windows (Conexión Ethernet)
* **Puerto Web UI:** `8000` (`http://localhost:8000`)
* **Puerto REST API:** `8089` (Utilizado por `check_bruteforce.py`)
* **Puerto Ingestion:** `9997` (Recepción desde Universal Forwarder)

---

## 🔌 Configuración del Ingestion (`Splunk_TA_nix`)

Dado el uso de la **licencia Free** de Splunk (que limita ciertas funciones nativas de la App de Unix), el Add-on `Splunk_TA_nix` se configuró manualmente para parsear los siguientes inputs desde Ubuntu:

* **Fuerza Bruta SSH & Sudo:** sourcetype `linux_secure` / `syslog` (`auth.log`)
* **Tráfico Web DVWA:** sourcetype `access_combined` (`access.log`)
* **Errores de Webserver / DoS:** sourcetype `apache_error` (`error.log`)
* **Lógica de Kernel & Archivos:** sourcetype `auditd` (`audit.log`)