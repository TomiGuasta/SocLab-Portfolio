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

> **Nota de Seguridad:** Estos archivos contienen configuraciones diseñadas para un entorno de laboratorio aislado. No aplicar estas configuraciones en entornos de producción sin una revisión de seguridad y adaptación a las necesidades específicas.
