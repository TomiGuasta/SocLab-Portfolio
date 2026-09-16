# Matriz de Riesgos ISO 27005

Esta matriz centraliza los riesgos de seguridad de la información identificados, evaluados y en tratamiento, según la metodología ISO 27005.

| Escenario de Ataque | Probabilidad (1-5) | Impacto (1-4) | Nivel de Riesgo | Plan de Tratamiento | Playbook Relacionado |
| :--- | :--- | :--- | :--- | :--- | :--- |
| *Ejemplo: SQLi* | *4* | *4* | *16 (Alto)* | [Ver Tratamiento](./Tratamiento/) | [SQLi](../../../homelab-soc/docs/DVWA-Attacks/SQL%20Injection%20+%20Hashing/Playbook-SQLInjection.md) |
| XSS | 4 | 3 | 12 (Alto) | [Ver Tratamiento](./Tratamiento/) | [XSS](../../Defense/01_Playbooks/Playbook-XSS.md) |
| Brute Force (DVWA) | 4 | 3 | 12 (Alto) | [Ver Tratamiento](./Tratamiento/) | [DVWA Brute Force](../../Defense/01_Playbooks/Playbook-DVWA-BruteForce.md) |
| Brute Force (Hydra) | 3 | 4 | 12 (Alto) | [Ver Tratamiento](./Tratamiento/) | [Hydra Brute Force](../../Defense/01_Playbooks/Playbook-Hydra-BruteForce.md) |
| Nmap (Reconocimiento) | 5 | 2 | 10 (Alto) | [Ver Tratamiento](./Tratamiento/) | [Nmap](../../Defense/01_Playbooks/Playbook-Nmap.md) |

## Metodología
- **Cálculo:** Probabilidad (1-5) * Impacto (1-4) = Nivel de Riesgo.
- **Severidad:**
  - **Bajo (1-4):** Riesgo aceptable.
  - **Medio (5-9):** Requiere monitoreo.
  - **Alto (10-20):** Requiere plan de tratamiento inmediato.

---
*Para más detalles, consultar [Metodologia.md](./Metodologia.md).*
