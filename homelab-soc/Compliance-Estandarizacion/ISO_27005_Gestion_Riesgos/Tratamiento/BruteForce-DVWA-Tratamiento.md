# Tratamiento de Riesgo: Brute Force (DVWA)

## 1. Estrategia de Tratamiento (ISO 27005)
- [x] Mitigación (Aplicar controles)
- [ ] Transferencia (Seguro, tercero)
- [ ] Aceptación (Riesgo residual aceptado)
- [ ] Evitación (Eliminar el servicio/proceso)

## 2. Controles Asociados (ISO 27002)
- **Control A.8.25 (Desarrollo seguro):** Implementar mecanismos de bloqueo de cuenta tras N intentos fallidos e integración de CAPTCHA.
- **Control A.8.26 (Seguridad de aplicaciones):** Configuración de un WAF o limitador de tasa (rate limiting) para peticiones al endpoint de autenticación.

## 3. Plan de Acción
- [ ] Implementar políticas de lockout en la aplicación DVWA.
- [ ] Configurar reglas en el SIEM para alertar sobre intentos masivos de inicio de sesión fallidos.
- [ ] Realizar pruebas de penetración enfocadas en fuerza bruta para verificar la efectividad de los bloqueos.

## 4. Riesgo Residual
- Probabilidad Estimada: 2
- Impacto Estimado: 2
- Nivel de Riesgo Residual: 4 (Bajo)

## 5. Contexto de Adversario (MITRE ATT&CK)
- Técnica local: [T1110.001 - Brute Force: Password Guessing](../../../../MITRE/02 - Técnicas/T1110 - Brute Force.md)
- Link Oficial: [MITRE ATT&CK - Password Guessing](https://attack.mitre.org/techniques/T1110/001/)

---
*Referencia técnica: [Playbook DVWA BruteForce](../../Defense/01_Playbooks/Playbook-DVWA-BruteForce.md)*
