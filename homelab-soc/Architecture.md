# 🏗️ Arquitectura del Laboratorio (SOC Lab)

Este documento detalla la estructura lógica y física de mi entorno de pruebas de ciberseguridad, consolidando la información del proyecto y los recursos relacionados.

## 🗺️ Diagrama de Arquitectura

```mermaid
graph TB
    %% Definición de Estilos
    classDef attacker fill:#fdd,stroke:#f00,stroke-width:2px;
    classDef victim fill:#dfd,stroke:#0f0,stroke-width:2px;
    classDef siem fill:#ddf,stroke:#00f,stroke-width:2px;

    subgraph Internet_Zone [Simulated Network 192.168.0.x]
        KALI[Kali Linux<br/>Attacker<br/>192.168.0.x]:::attacker
    end

    subgraph Defense_Lab [Lab Network 192.168.1.x]
        subgraph Victim_Host [Ubuntu Server 192.168.1.x]
            DVWA[App: DVWA]
            FW[Python Firewall + Iptables]
            AUDITD[Auditd Logger]
        end
        SPLUNK[Splunk SIEM<br/>192.168.1.x]:::siem
    end

    %% Flujos de Ataque
    KALI -- "Exploitation<br/>(HTTP/SSH)" --> DVWA

    %% Flujos de Defensa / Logs
    DVWA --> FW
    FW -.-> |"Intercept/Filter"| DVWA
    AUDITD --> |"Syslogs"| SPLUNK
    DVWA --> |"App Logs"| SPLUNK

    %% Inteligencia
    SPLUNK -- "API Request" --> THREAT[External Threat Intel]
```

## 📋 Componentes

### 1. Zona de Ataque (Red Externa)
*   **Kali Linux:** Máquina virtual utilizada como nodo de ataque para simular vectores reales (Fuerza bruta, escaneos, fuzzing web).

### 2. Zona de Defensa (Red del Laboratorio)
*   **Ubuntu Server (Víctima):** Aloja la aplicación vulnerable (**DVWA**).
    *   **Firewall Personalizado:** Script de Python que interactúa con `iptables` para bloqueo estático y detección de anomalías.
    *   **Auditd:** Monitoreo de actividad a nivel del sistema operativo.
*   **Splunk SIEM:** Servidor centralizado para la ingesta y análisis de logs (`Syslogs` del sistema y logs de aplicación).
    *   Utiliza consultas (SPL) para la detección de comportamientos sospechosos y alertas.
    *   Integración con fuentes externas para Threat Intelligence.

---

## 📚 Información del Proyecto y Recursos

Repositorio con mis proyectos de práctica en ciberseguridad con enfoque defensivo pero también tratando con la parte de ataque, documentando el proceso de aprendizaje desde ejercicios introductorios hasta un entorno de detección completo con SIEM, que es el que actualmente estoy trabajando.

- **Documentación de Ataques y Playbooks**: Accede a la documentación completa en GitHub: [Ver Documentación y Playbooks](https://github.com/TomiGuasta/SocLab-Portfolio/tree/main/homelab-soc/docs)

### 📂 Proyectos principales

#### [`homelab-soc/`]
Laboratorio de detección propio, montado desde cero con Kali Linux, Ubuntu Server y Splunk Enterprise. Simulo ataques reales (fuerza bruta SSH, escaneo de puertos, fuzzing web, explotación de una aplicación vulnerable) y construyo las detecciones correspondientes: reglas de auditoría, queries SPL, y documentación de cada hallazgo con su análisis y remediación. Es mi proyecto principal — el que mejor refleja cómo trabajo end-to-end, desde generar el ataque hasta detectarlo y explicar por qué importa.
