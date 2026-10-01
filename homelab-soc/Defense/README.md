---
tags: [siem, splunk, alerts, savedsearches, blue-team, detection, telegram]
fecha: 2026-10-01
componente: Splunk SIEM - Automation & Telegram Notifications
---

# 🚨 Automatización de Alertas en Splunk con Notificaciones por Telegram (`savedsearches.conf` & `telegram_alert.py`)

Este directorio contiene la configuración de búsquedas guardadas y alertas automatizadas (`savedsearches.conf`), así como el script disparador en Python (`telegram_alert.py`) para enviar notificaciones en tiempo real directamente a un canal o chat de Telegram cuando se detectan amenazas en el Home Lab.

## 📁 Estructura
- `savedsearches.conf`: Configuración nativa de Splunk con alertas habilitadas para ejecutar el script de notificación.
- `telegram_alert.py`: Script en Python encargado de procesar los resultados de Splunk y enviarlos formateados mediante la API de Telegram Bot.

## ⚙️ Reglas de Detección Incluidas

1. **SSH Brute Force (`ssh_brute_force_detection`)** - Severidad Media (3)
2. **DVWA Web Brute Force (`dvwa_brute_force_detection`)** - Severidad Media (3)
3. **GoBuster / Fuzzing Directory Scanning (`gobuster_fuzzing_detection`)** - Severidad Baja/Media (2)
4. **SQL Injection (`sql_injection_detection`)** - Severidad Alta (4)
5. **Cross-Site Scripting XSS (`xss_attack_detection`)** - Severidad Media (3)
6. **Auditd Critical File Modification (`auditd_sensitive_file_modification`)** - Severidad Crítica (5)

---

## 🛠️ Instrucciones de Despliegue e Integración con Telegram

### 1. Configurar el Bot de Telegram
1. Habla con [@BotFather](https://t.me/BotFather) en Telegram para crear un nuevo bot y obtener tu **Bot Token**.
2. Obtén el **Chat ID** del chat o canal donde deseas recibir las alertas (puedes usar bots como `@userinfobot` o la API `getUpdates`).

### 2. Desplegar los archivos en Splunk Enterprise
Copia los archivos en el directorio de la aplicación `search` de tu servidor Splunk (por ejemplo, `/opt/splunk/etc/apps/search/local/`):

1. **Copiar el script de alerta:**
   ```bash
   cp telegram_alert.py /opt/splunk/bin/scripts/
   chmod +x /opt/splunk/bin/scripts/telegram_alert.py
   ```

2. **Configurar credenciales en variables de entorno de Splunk** (o editar directamente el script con tus valores):
   Puedes exportar las variables en el entorno del servicio de Splunk (`/opt/splunk/etc/splunk-launch.conf` o systemd service):
   ```env
   TELEGRAM_BOT_TOKEN="TU_BOT_TOKEN_AQUÍ"
   TELEGRAM_CHAT_ID="TU_CHAT_ID_AQUÍ"
   ```

3. **Copiar la configuración de alertas:**
   ```bash
   cp savedsearches.conf /opt/splunk/etc/apps/search/local/savedsearches.conf
   ```

4. **Probar el envío manual del script:**
   ```bash
   python3 /opt/splunk/bin/scripts/telegram_alert.py --test
   ```

5. **Reiniciar Splunk o recargar configuración:**
   ```bash
   /opt/splunk/bin/splunk restart
   ```
