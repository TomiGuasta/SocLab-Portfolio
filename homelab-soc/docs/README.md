# Documentación del SOC - Laboratorio
Bienvenido a la documentación técnica de los ataques realizados en el Laboratorio SOC.

## Diagrama de Ataques
```mermaid
graph TD
    A[Inicio: SOC Lab] --> B[Ataques Playbooks]
    B --> C[Nmap]
    B --> D[Hydra]
    B --> E[GoBuster]
    B --> F[DVWA: Brute Force]
    B --> G[DVWA: DoS]
    B --> H[DVWA: Fuzzing]
    B --> I[DVWA: SQL Injection]
    B --> J[DVWA: XSS]
    
    click C "https://github.com/TomiGuasta/SocLab-Portfolio/tree/main/homelab-soc/docs/Nmap%20-%20PortScan"
    click D "https://github.com/TomiGuasta/SocLab-Portfolio/tree/main/homelab-soc/docs/Hydra%20-%20BruteForce"
    click E "https://github.com/TomiGuasta/SocLab-Portfolio/tree/main/homelab-soc/docs/GoBuster%20-%20Fuzzing"
    click F "https://github.com/TomiGuasta/SocLab-Portfolio/tree/main/homelab-soc/docs/DVWA-Attacks/BruteForce"
    click G "https://github.com/TomiGuasta/SocLab-Portfolio/tree/main/homelab-soc/docs/DVWA-Attacks/DoS"
    click H "https://github.com/TomiGuasta/SocLab-Portfolio/tree/main/homelab-soc/docs/DVWA-Attacks/Fuzzing"
    click I "https://github.com/TomiGuasta/SocLab-Portfolio/tree/main/homelab-soc/docs/DVWA-Attacks/SQL%20Injection%20%2B%20Hashing"
    click J "https://github.com/TomiGuasta/SocLab-Portfolio/tree/main/homelab-soc/docs/DVWA-Attacks/XSS"
```

## Índice de Ataques
- [Nmap - PortScan](https://github.com/TomiGuasta/SocLab-Portfolio/tree/main/homelab-soc/docs/Nmap%20-%20PortScan)
- [Hydra - BruteForce](https://github.com/TomiGuasta/SocLab-Portfolio/tree/main/homelab-soc/docs/Hydra%20-%20BruteForce)
- [GoBuster - Fuzzing](https://github.com/TomiGuasta/SocLab-Portfolio/tree/main/homelab-soc/docs/GoBuster%20-%20Fuzzing)
- [DVWA - Brute Force](https://github.com/TomiGuasta/SocLab-Portfolio/tree/main/homelab-soc/docs/DVWA-Attacks/BruteForce)
- [DVWA - DoS](https://github.com/TomiGuasta/SocLab-Portfolio/tree/main/homelab-soc/docs/DVWA-Attacks/DoS)
- [DVWA - Fuzzing](https://github.com/TomiGuasta/SocLab-Portfolio/tree/main/homelab-soc/docs/DVWA-Attacks/Fuzzing)
- [DVWA - SQL Injection + Hashing](https://github.com/TomiGuasta/SocLab-Portfolio/tree/main/homelab-soc/docs/DVWA-Attacks/SQL%20Injection%20%2B%20Hashing)
- [DVWA - XSS](https://github.com/TomiGuasta/SocLab-Portfolio/tree/main/homelab-soc/docs/DVWA-Attacks/XSS)
