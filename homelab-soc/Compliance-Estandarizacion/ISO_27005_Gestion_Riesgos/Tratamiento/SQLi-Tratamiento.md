# Tratamiento de Riesgo: SQL Injection

## 1. Estrategia de Tratamiento (ISO 27005)
- [x] Mitigación (Aplicar controles)
- [ ] Transferencia (Seguro, tercero)
- [ ] Aceptación (Riesgo residual aceptado)
- [ ] Evitación (Eliminar el servicio/proceso)

## 2. Controles Asociados (ISO 27002)
- **Control A.8.25 (Desarrollo seguro):** Implementar validación de entradas y uso de sentencias parametrizadas.
- **Control A.8.26 (Seguridad de aplicaciones):** Configuración de un Web Application Firewall (WAF) para filtrar peticiones maliciosas.

## 3. Plan de Acción
- [ ] Revisar y asegurar todas las consultas SQL en la aplicación objetivo (ej. DVWA).
- [ ] Implementar y configurar una regla de bloqueo en el WAF/SIEM para patrones de SQLi conocidos.
- [ ] Realizar pruebas de penetración periódicas para verificar la efectividad de los controles.

## 4. Riesgo Residual
- Probabilidad Estimada: 2
- Impacto Estimado: 2
- Nivel de Riesgo Residual: 4 (Bajo)

## 5. Contexto de Adversario (MITRE ATT&CK)
- Técnica local: [T1190 - Exploit Public-Facing Application](../../../../MITRE/02 - Técnicas/T1190 - Exploit Public-Facing Application.md)
- Link Oficial: [MITRE ATT&CK - SQL Injection](https://attack.mitre.org/techniques/T1190/)

---
