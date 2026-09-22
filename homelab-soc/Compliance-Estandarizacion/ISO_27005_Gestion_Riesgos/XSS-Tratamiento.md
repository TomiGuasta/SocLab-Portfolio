# Tratamiento de Riesgo: Cross-Site Scripting (XSS)

## 1. Estrategia de Tratamiento (ISO 27005)
- [x] Mitigación (Aplicar controles)
- [ ] Transferencia (Seguro, tercero)
- [ ] Aceptación (Riesgo residual aceptado)
- [ ] Evitación (Eliminar el servicio/proceso)

## 2. Controles Asociados (ISO 27002)
- **Control A.8.25 (Desarrollo seguro):** Implementar codificación de salida (output encoding) para prevenir la ejecución de scripts maliciosos.
- **Control A.8.26 (Seguridad de aplicaciones):** Implementar políticas de seguridad de contenido (CSP - Content Security Policy).

## 3. Plan de Acción
- [ ] Auditar las aplicaciones para identificar puntos de inyección de scripts en formularios y parámetros de URL.
- [ ] Implementar la codificación de caracteres en todas las salidas del lado del cliente.
- [ ] Configurar cabeceras CSP estrictas en el servidor web.

## 4. Riesgo Residual
- Probabilidad Estimada: 2
- Impacto Estimado: 2
- Nivel de Riesgo Residual: 4 (Bajo)

## 5. Contexto de Adversario (MITRE ATT&CK)
- Técnica local: [T1190 - Exploit Public-Facing Application](../../../../MITRE/02 - Técnicas/T1190 - Exploit Public-Facing Application.md)
- Link Oficial: [MITRE ATT&CK - XSS](https://attack.mitre.org/techniques/T1189/)

---
*Referencia técnica: [Playbook XSS](../../Defense/01_Playbooks/Playbook-XSS.md)*
