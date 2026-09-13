# 📋 Infraestructura y Configuración (IT)

Este directorio contiene la documentación técnica y las plantillas de configuración (IaC - Infrastructure as Code) para los componentes fundamentales del **SOC Home Laboratory**. Estas configuraciones permiten el despliegue y monitoreo de un entorno controlado para el estudio de ciberseguridad, simulación de ataques y análisis de defensa.

## 📂 Contenido del Directorio

| Archivo | Descripción |
| :--- | :--- |
| [`Auditd-Rules.md`](Auditd-Rules.md) | Reglas críticas de auditoría de kernel (`auditd`) para monitoreo de integridad y cambios en el sistema operativo. |
| [`Setup Kali-Linux.md`](Setup%20Kali-Linux.md) | Configuración y herramientas del host **Atacante** utilizado para la simulación de escenarios de *Red Team*. |
| [`Setup Splunk-SIEM.md`](Setup%20Splunk-SIEM.md) | Configuración del servidor SIEM para centralización, ingesta y análisis de telemetría de logs. |
| [`Setup Ubuntu-Server.md`](Setup%20Ubuntu-Server.md) | Configuración del host **Víctima** que aloja servicios vulnerables (DVWA, Apache, etc.) para ejercicios de defensa. |

---

## 📖 Detalles de los Componentes

### 🛡️ Auditd-Rules.md
Documenta la implementación de reglas de auditoría a nivel de kernel utilizando `auditd`. El objetivo es capturar eventos críticos del sistema operativo, tales como modificaciones en archivos de autenticación (`/etc/passwd`, `/etc/shadow`), cambios en configuraciones de red (`sshd_config`) y la ejecución de comandos con privilegios elevados (`sudo`), proporcionando visibilidad sobre actividades potencialmente maliciosas.

### ⚔️ Setup Kali-Linux.md
Describe la configuración del host atacante dentro del entorno de laboratorio. Incluye detalles sobre la configuración de red y un catálogo de herramientas esenciales para el ejercicio de *Red Team*, tales como `nmap` y `gobuster` para reconocimiento, `hydra` para fuerza bruta, y herramientas para explotación web y DoS. También establece directrices de seguridad para el manejo de este host.

### 📊 Setup Splunk-SIEM.md
Detalla la infraestructura del servidor SIEM (Splunk Enterprise), responsable de la centralización y análisis de telemetría. Incluye información sobre los puertos de comunicación, la configuración de ingestión de datos mediante el Add-on `Splunk_TA_nix` y los tipos de logs (`sourcetypes`) recopilados (seguridad Linux, logs de Apache, auditoría de kernel), permitiendo la correlación de eventos y la detección de amenazas.

### 🖥️ Setup Ubuntu-Server.md
Presenta la configuración del host víctima, el cual aloja las aplicaciones y servicios vulnerables para las pruebas de penetración (ej. DVWA). Documenta la arquitectura de los servicios expuestos (SSH, Apache, MariaDB), la integración del agente de logs con el SIEM y las configuraciones de seguridad (hardening) necesarias para mantener la integridad del laboratorio mientras se simulan ataques.
