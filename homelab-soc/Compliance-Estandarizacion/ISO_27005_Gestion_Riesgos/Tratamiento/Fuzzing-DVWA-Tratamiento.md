---
tipo: "Tratamiento"
ataque: "Fuzzing"
herramienta: "FFUF (DVWA)"
fecha: 2026-09-23
estado: "Documentado"
---

# Tratamiento: Fuzzing (DVWA)

## 1. Definición del Riesgo
El fuzzing contra DVWA busca descubrir archivos o directorios ocultos que puedan contener vulnerabilidades o información sensible, facilitando ataques posteriores.

## 2. Medidas de Mitigación (ISO 27002 / Controles)
*   **A.12.6.1 (Gestión de vulnerabilidades técnicas):** Mantener el software actualizado y parcheado.
*   **A.13.1.1 (Controles de red):** Implementar WAF para detectar y bloquear patrones de escaneo conocidos.
*   **A.9.1.1 (Política de control de acceso):** Restringir el acceso a directorios administrativos solo a direcciones IP autorizadas.

## 3. Estrategia de Respuesta (Playbook Integrado)
*   **Detección:** Basado en `Playbook-DVWA-Fuzzing.md`, monitorizar logs de acceso (Apache) buscando alta frecuencia de códigos 404.
*   **Contención:** Bloqueo automático mediante WAF/Firewall tras detectar el umbral de errores.

## 4. Riesgo Residual
*   **Medio:** A pesar del bloqueo, un atacante persistente podría utilizar técnicas de *evasión* (menor tasa de peticiones, uso de proxies) para evadir la detección basada en umbrales simples.
