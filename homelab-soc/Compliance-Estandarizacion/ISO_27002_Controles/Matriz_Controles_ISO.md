# Matriz de Mapeo ISO 27002:2022 - Controles Técnicos

Este documento mapea los **Playbooks de Defensa** existentes en el laboratorio con los controles técnicos de la norma **ISO/IEC 27002:2022**.

| ID ISO | Control | Descripción Técnica (ISO 27002) | Playbook Relacionado | Evidencia de Control | Responsable | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **8.15** | Registro de eventos | Eventos de seguridad (logs) registrados, protegidos y revisados para detectar anomalías. | `[Todos (SIEM)]` | `[Link a Logs/SIEM]` | CISO / Lab Admin | En revisión |
| **8.16** | Monitoreo de actividades | Monitoreo de sistemas para detectar comportamiento inusual (ataques, acceso no autorizado). | `[Playbook-Nmap]` | `[Link a Alertas]` | CISO / Lab Admin | Implementado |
| **8.8** | Gestión de vulnerabilidades | Identificación y tratamiento de vulnerabilidades técnicas en infraestructura y aplicaciones. | `[Playbook-DVWA]` | `[Link a Escaneos]` | CISO / Lab Admin | Pendiente |
| **5.15** | Control de acceso | Restricción de acceso a información y activos según necesidad (principio mínimo privilegio). | `[Playbook-Hydra]` | `[Link a Config]` | CISO / Lab Admin | En revisión |
| **8.20** | Seguridad de redes | Gestión de seguridad de redes y segregación para proteger activos de información. | `[Playbook-DoS]` | `[Link a Firewalls]` | CISO / Lab Admin | Pendiente |

## Notas de Mapeo
- **Evidencia**: Debe apuntar a reportes, capturas de pantalla o logs del laboratorio.
- **Estado**: (Pendiente / En revisión / Implementado / No aplica).
- **ISO 27002:2022**: Esta matriz se basa en los controles del Anexo A de ISO 27001 (derivados de ISO 27002:2022).
