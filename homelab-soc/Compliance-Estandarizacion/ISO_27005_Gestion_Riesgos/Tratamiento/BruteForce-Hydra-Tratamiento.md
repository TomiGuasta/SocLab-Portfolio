# Tratamiento de Riesgo: Brute Force (Hydra)

## 1. Estrategia de Tratamiento (ISO 27005)
- [x] Mitigación (Aplicar controles)
- [ ] Transferencia (Seguro, tercero)
- [ ] Aceptación (Riesgo residual aceptado)
- [ ] Evitación (Eliminar el servicio/proceso)

## 2. Controles Asociados (ISO 27002)
- **Control A.8.25 (Desarrollo seguro):** Políticas de contraseñas robustas, implementación obligatoria de MFA en servicios críticos.
- **Control A.8.26 (Seguridad de aplicaciones):** Implementación de rate-limiting (fail2ban) en servicios SSH y web, monitoreo activo de logs de autenticación.

## 3. Plan de Acción
- [ ] Configurar herramientas de prevención automática (fail2ban) para bloquear IPs tras intentos fallidos.
- [ ] Implementar MFA en servicios expuestos (SSH/Web).
- [ ] Auditar y rotar credenciales comprometidas o débiles regularmente.

## 4. Riesgo Residual
- Probabilidad Estimada: 2
- Impacto Estimado: 3
- Nivel de Riesgo Residual: 6 (Medio)

## 5. Contexto de Adversario (MITRE ATT&CK)
- Técnica local: [T1110.001 - Brute Force: Password Guessing](../../../../MITRE/02 - Técnicas/T1110 - Brute Force.md)
- Link Oficial: [MITRE ATT&CK - Password Guessing](https://attack.mitre.org/techniques/T1110/001/)

---
*Referencia técnica: [Playbook Hydra BruteForce](../../Defense/01_Playbooks/Playbook-Hydra-BruteForce.md)*
