---
tipo: "Tratamiento"
ataque: "Reconocimiento"
herramienta: "Nmap"
fecha: 2026-09-24
estado: "Documentado"
---

# Tratamiento: Reconocimiento (Nmap)

## 1. Definición del Riesgo
El escaneo de puertos permite a un atacante identificar servicios activos, versiones de software y potenciales puntos de entrada, facilitando la planificación de ataques dirigidos.

## 2. Medidas de Mitigación (ISO 27002 / Controles)
*   **A.9.1.1 (Política de control de acceso):** Minimización de la superficie de ataque; cerrar todos los puertos y servicios que no sean estrictamente necesarios.
*   **A.13.1.1 (Controles de red):** Implementar IDS/IPS para detectar patrones de escaneo y bloquear proactivamente IPs sospechosas.
*   **A.12.4.1 (Registro de eventos):** Monitorear logs de firewall (`ufw.log` o `iptables`) para detectar intentos de conexión masiva.

## 3. Estrategia de Respuesta (Playbook Integrado)
*   **Detección:** Basado en `Playbook-Nmap.md`, monitorizar alertas de seguridad por tráfico inusual (alto volumen de intentos de conexión desde una IP).
*   **Contención:** Bloqueo preventivo de la IP origen en Firewall tras identificar comportamiento de escaneo.

## 4. Riesgo Residual
*   **Bajo/Medio:** El reconocimiento pasivo o técnicas de escaneo muy lentas/evasivas (ej. `-T0`, `-T1`) pueden no ser detectados por los controles estándar de red.
