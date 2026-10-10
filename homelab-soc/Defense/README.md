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

---

## 🔍 ¿Cómo Funciona el Sistema de Alertas y Notificaciones? (Funcionamiento Interno)

El flujo operativo entre Splunk y Telegram opera de forma totalmente automatizada mediante el siguiente pipeline:

1. **Evaluación Programada:** Las reglas definidas en `savedsearches.conf` se ejecutan periódicamente en Splunk según su frecuencia programada (`cron_schedule`, por ejemplo, cada 1 o 5 minutos).
2. **Disparador de Alerta (Trigger):** Si una consulta SPL detecta anomalías que superan el umbral establecido (ej. más de 5 intentos fallidos de SSH o patrones de Inyección SQL), Splunk activa la alerta.
3. **Ejecución del Script (`action.script = 1`):** En lugar de depender de correo electrónico, Splunk invoca de forma nativa el script Python configurado:
   - **Script:** `telegram_alert.py`
   - **Paso de Parámetros:** Splunk pasa automáticamente argumentos al script al momento de la ejecución (`$1`: ruta del archivo de resultados CSV, `$2`: número de eventos/conteo, `$3`: razón del disparo, `$4`: nombre de la alerta, `$5`: descripción).
4. **Procesamiento y Mapeo de Severidad:** El script lee los argumentos de entrada, evalúa el nombre de la alerta para asignar un nivel de severidad y un emoji representativo (`🚨🔥` para Crítico/Alto, `⚠️` para Medio, `ℹ️` para Bajo).
5. **Envío a Telegram via API HTTP POST:** Mediante la librería estándar de Python (`urllib.request`), el script empaqueta la alerta con formato Markdown y realiza una petición segura (`https://api.telegram.org/bot<TOKEN>/sendMessage`) hacia el chat o grupo configurado.

---

## ⚙️ Reglas de Detección Incluidas

1. **SSH Brute Force (`ssh_brute_force_detection`)**
   - **Severidad:** Media (3) | **Frecuencia:** Cada 5 min.
   - **SPL:** `index=main (sourcetype=linux_secure OR sourcetype=auth) "Failed password" | stats count by src_ip, user | where count >= 5`

2. **DVWA Web Brute Force (`dvwa_brute_force_detection`)**
   - **Severidad:** Media (3) | **Frecuencia:** Cada 5 min.
   - **SPL:** `index=main sourcetype=access_combined status=401 | stats count by clientip, uri | where count > 10`

3. **GoBuster / Fuzzing Directory Scanning (`gobuster_fuzzing_detection`)**
   - **Severidad:** Baja/Media (2) | **Frecuencia:** Cada 5 min.
   - **SPL:** `index=main sourcetype=access_combined (status=404 OR status=403) | stats count by clientip | where count > 50`

4. **SQL Injection (`sql_injection_detection`)**
   - **Severidad:** Alta (4) | **Frecuencia:** Cada 1 min.
   - **SPL:** `index=main sourcetype=access_combined (uri="*UNION*SELECT*" OR uri="*OR*=*'") | stats count by clientip, uri`

5. **Cross-Site Scripting XSS (`xss_attack_detection`)**
   - **Severidad:** Media (3) | **Frecuencia:** Cada 1 min.
   - **SPL:** `index=main sourcetype=access_combined (uri="*%3Cscript%3E*") | stats count by clientip, uri`

6. **Auditd Critical File Modification (`auditd_sensitive_file_modification`)**
   - **Severidad:** Crítica (5) | **Frecuencia:** Cada 5 min.
   - **SPL:** `index=main (key=passwd_changes OR key=shadow_changes OR key=sudoers_changes) | table _time, host, exe, uid, success, key`

---

## 🛠️ Instrucciones de Despliegue e Integración

### 1. Configurar el Bot de Telegram
1. Habla con [@BotFather](https://t.me/BotFather) en Telegram para crear un nuevo bot y obtener tu **Bot Token**.
2. Obtén el **Chat ID** del chat o canal donde deseas recibir las alertas (puedes usar bots como `@userinfobot` o consultando la API `getUpdates`).

### 2. Desplegar los archivos en Splunk Enterprise
Copia los archivos en el directorio de la aplicación `search` de tu servidor Splunk (por defecto `/opt/splunk/etc/apps/search/local/`):

1. **Copiar el script de alerta al directorio bin de Splunk:**
   ```bash
   cp telegram_alert.py /opt/splunk/bin/scripts/
   chmod +x /opt/splunk/bin/scripts/telegram_alert.py
   ```

2. **Configurar credenciales en variables de entorno de Splunk** (o editar directamente el script con tus valores):
   Puedes exportar las variables en el entorno del servicio de Splunk (`/opt/splunk/etc/splunk-launch.conf` o archivo de systemd):
   ```env
   TELEGRAM_BOT_TOKEN="TU_BOT_TOKEN_AQUÍ"
   TELEGRAM_CHAT_ID="TU_CHAT_ID_AQUÍ"
   ```

3. **Copiar la configuración de alertas:**
   ```bash
   cp savedsearches.conf /opt/splunk/etc/apps/search/local/savedsearches.conf
   ```

4. **Probar el funcionamiento manual del script:**
   ```bash
   python3 /opt/splunk/bin/scripts/telegram_alert.py --test
   ```

5. **Reiniciar Splunk o recargar configuración:**
   ```bash
   /opt/splunk/bin/splunk restart
   ```

---

## 💡 Alternativa para Splunk Free: Poller por API REST (`splunk_poller.py`)

Como se mencionó anteriormente, la versión gratuita de Splunk (Splunk Free) deshabilita las acciones de alerta programadas (`savedsearches.conf`). Para superar esta limitación en un entorno de laboratorio sin incurrir en costos de licencia, se desarrolló **`splunk_poller.py`**.

### ¿Cómo funciona el Poller Externo?
En lugar de depender del programador interno de Splunk:
1. **Consulta Programada:** Se ejecuta de forma externa (mediante el Programador de Tareas de Windows o un `cron` job en Linux) cada 5 minutos.
2. **API REST de Splunk:** Se conecta mediante HTTPS (`https://localhost:8089/services/search/jobs/oneshot`) utilizando autenticación HTTP Basic.
3. **Evaluación de Eventos:** Ejecuta las consultas SPL de detección directamente contra el motor de Splunk y evalúa si el conteo de resultados es mayor a 0 (`count > 0`).
4. **Despacho a Telegram:** Si encuentra actividad maliciosa, genera y envía inmediatamente la alerta formateada con Markdown a Telegram.

### Configuración de Credenciales en `splunk_poller.py`
Abre `splunk_poller.py` y configura tus credenciales reales:
```python
SPLUNK_PASSWORD = "tu_password_de_splunk"
BOT_TOKEN = "tu_token_de_botfather"
CHAT_ID = "tu_chat_id_numerico"
```

### Despliegue y Automatización en Windows
1. **Programar tarea en Windows (Task Scheduler):**
   - Crear una Tarea llamada `SplunkPoller`.
   - Disparador: Repetir cada 5 minutos indefinidamente.
   - Acción: Iniciar un programa -> `python.exe` con argumento `D:\Obsidian\CiberSecurity Portfolio\Portfolio\Defense\02_SIEM\splunk_poller.py`.
   - Iniciar en: `D:\Obsidian\CiberSecurity Portfolio\Portfolio\Defense\02_SIEM\`

---

## 🛡️ Consulta SIEM para Firewall / Active Response (SOAR)

Para auditar y visualizar en tiempo real las IPs bloqueadas por el firewall virtual y aplicadas en el kernel mediante `iptables`, puedes utilizar la siguiente consulta SPL en Splunk:

```spl
index=firewall action=block OR action=drop 
| stats count by src_ip, dest_ip, reason 
| sort - count
```

### Correlación con `iptables`
Cuando ejecutas en el servidor Ubuntu la validación de reglas activas:
```bash
sudo iptables -S
```
Verás las reglas en crudo del kernel (ej: `-A INPUT -s 192.168.0.36 -j DROP`). La consulta SPL anterior mapea exactamente esas IPs (`src_ip`), el destino protegido (`dest_ip`), el motivo o comentario de la detección (`reason`) y la cantidad de intentos bloqueados (`count`), unificando la visibilidad del SIEM con el enforcement del SOAR.


