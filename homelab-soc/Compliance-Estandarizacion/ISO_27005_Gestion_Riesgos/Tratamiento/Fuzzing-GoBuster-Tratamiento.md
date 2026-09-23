---
tipo: "Tratamiento"
ataque: "Fuzzing"
herramienta: "GoBuster"
fecha: 2026-09-23
estado: "Documentado"
---

# Tratamiento: Fuzzing (GoBuster)

## 1. Definición del Riesgo
El uso de GoBuster permite el descubrimiento rápido de directorios y archivos en el servidor web, lo cual expone la estructura interna y posibles archivos sensibles (backups, configuraciones).

## 2. Medidas de Mitigación (ISO 27002 / Controles)
*   **A.12.1.2 (Gestión de cambios):** Asegurar que las versiones de desarrollo o archivos temporales no se desplieguen en entornos de producción.
*   **A.13.1.1 (Controles de red):** Implementar reglas de firewall para limitar la frecuencia de peticiones desde una misma dirección IP (rate-limiting).
*   **A.12.4.1 (Registro de eventos):** Monitoreo activo de logs de error (404) para identificar intentos de escaneo.

## 3. Estrategia de Respuesta (Playbook Integrado)
*   **Detección:** Basado en `Playbook-GoBuster-Fuzzing.md`, identificar secuencias rápidas de códigos 404 seguidas de éxitos (200) desde una IP.
*   **Contención:** Bloqueo de la IP en el firewall (`ufw` o `iptables`) e inspección de los recursos accedidos con éxito.

## 4. Riesgo Residual
*   **Bajo-Medio:** Un atacante puede utilizar listas de palabras (wordlists) altamente personalizadas o escaneo distribuido para evitar la detección por frecuencia.
