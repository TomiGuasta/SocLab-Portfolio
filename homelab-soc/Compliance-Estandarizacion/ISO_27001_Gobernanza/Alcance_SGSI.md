# Alcance del Sistema de Gestión de Seguridad de la Información (SGSI)

## 1. Perímetro Organizacional
El SGSI cubre todas las actividades de investigación, desarrollo de playbooks, pruebas de penetración controladas y monitoreo defensivo ejecutadas dentro del **Home Lab de Ciberseguridad**.

## 2. Activos Incluidos en el Alcance
1. **Infraestructura de Red y Servidores:**
   - Red virtual aislada del laboratorio.
   - Servidor Ubuntu (host objetivo y servicios web).
   - Contenedores Docker (DVWA, aplicaciones vulnerables).
2. **Estaciones de Trabajo / Herramientas:**
   - Kali Linux (herramientas ofensivas: Nmap, Hydra, Gobuster, SQLmap, etc.).
3. **Monitoreo y SIEM:**
   - Instancia de Splunk para análisis de logs y alertas.
   - Auditorías del sistema (`auditd`).
4. **Información Documentada:**
   - Este repositorio de Obsidian (Playbooks, matrices de riesgo, matrices de controles y documentación táctica de MITRE ATT&CK).

## 3. Exclusiones
- Redes personales externas o dispositivos ajenos al entorno de pruebas aislado.
