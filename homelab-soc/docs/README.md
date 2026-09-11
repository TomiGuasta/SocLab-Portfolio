# Documentación del SOC - Laboratorio
Bienvenido a la documentación técnica de los ataques realizados en el Laboratorio SOC.

## Diagrama de Ataques
```mermaid
graph TD
    A[Inicio: SOC Lab] --> B[Ataques Playbooks]
    B --> C[DoS]
    B --> D[Brute Force]
    B --> E[Fuzzing]
    B --> F[Escaneo]
    B --> G[Inyección SQL]
    B --> H[XSS]
    
    click C "../01_Playbooks/Playbook-DoS.md"
    click D "../01_Playbooks/Playbook-DVWA-BruteForce.md"
    click E "../01_Playbooks/Playbook-GoBuster-Fuzzing.md"
    click F "../01_Playbooks/Playbook-Nmap.md"
    click G "../01_Playbooks/Playbook-SQLInjection.md"
    click H "../01_Playbooks/Playbook-XSS.md"
```

## Índice de Ataques
- [DoS Attack](../01_Playbooks/Playbook-DoS.md)
- [Brute Force (DVWA)](../01_Playbooks/Playbook-DVWA-BruteForce.md)
- [Brute Force (Hydra)](../01_Playbooks/Playbook-Hydra-BruteForce.md)
- [Fuzzing (DVWA)](../01_Playbooks/Playbook-DVWA-Fuzzing.md)
- [Fuzzing (GoBuster)](../01_Playbooks/Playbook-GoBuster-Fuzzing.md)
- [Nmap Scan](../01_Playbooks/Playbook-Nmap.md)
- [SQL Injection](../01_Playbooks/Playbook-SQLInjection.md)
- [XSS](../01_Playbooks/Playbook-XSS.md)
