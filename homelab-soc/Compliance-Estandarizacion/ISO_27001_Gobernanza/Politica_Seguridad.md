# Política de Seguridad de la Información (SGSI)

## 1. Propósito y Objetivo
Esta política establece el marco general de seguridad de la información para el **Home Lab / Portafolio de Ciberseguridad**, asegurando la confidencialidad, integridad y disponibilidad de los activos de información, sistemas y simuladores de ataque/defensa.

## 2. Alcance
Aplica a todos los componentes del entorno de laboratorio:
- Máquinas virtuales de ataque (Kali Linux, herramientas de pentesting).
- Servidores objetivo e infraestructura defensiva (Ubuntu Server, contenedores Docker con DVWA, etc.).
- Sistemas de monitoreo y SIEM (Splunk).
- Documentación, playbooks y evidencias almacenadas en este repositorio.

## 3. Principios de Seguridad
1. **Confidencialidad:** Protección de credenciales, configuraciones y datos de prueba frente a exposiciones no autorizadas.
2. **Integridad:** Asegurar que los scripts, playbooks, reglas de auditoría y configuraciones del SIEM no sean alterados indebidamente.
3. **Disponibilidad:** Mantener operativo el entorno de pruebas para la validación continua de controles de seguridad.
4. **Cumplimiento y Legalidad:** Toda actividad ofensiva (pentesting / simulación) se realiza exclusivamente dentro del perímetro autorizado del Home Lab con fines educativos y de validación defensiva.

## 4. Responsabilidades
- **CISO / Administrador del Lab:** Responsable de la implementación, revisión y mantenimiento del SGSI, así como de la ejecución de playbooks de defensa y respuesta a incidentes.
- **Auditores / Evaluadores:** Responsables de verificar el cumplimiento de los controles técnicos (ISO 27002) y la correcta gestión de riesgos (ISO 27005).

## 5. Revisión
Esta política debe ser revisada al menos una vez al año o cuando se produzcan cambios significativos en la arquitectura del laboratorio.
