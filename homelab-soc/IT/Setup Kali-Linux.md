---
tags: [infraestructura, atacante, kali, red-team, tools]
fecha: 2026-08-31
componente: Host Atacante
hostname: kali-attacker-vm
ip_ejemplo: 192.168.1.10
rol: Red Team / Simulación de Amenazas
---

# ⚔️ Host Atacante: Kali Linux

## 🌐 Contexto de Red (IaC Template)
Configurar la interfaz de red en modo *Bridged* o *NAT* según el aislamiento requerido para el laboratorio.

* **Dirección IP:** `{{ATTACKER_IP}}` (Ejemplo: `192.168.1.10`)
* **SO:** Kali Linux (64-bit)

## 🛠️ Toolkit de Simulación
Herramientas instaladas para el desarrollo de ejercicios de Red Team:

* **Escaneo y Reconocimiento:** `nmap`, `gobuster`
* **Fuerza Bruta & Credenciales:** `hydra`, `hashcat`
* **Explotación Web & PoC:** `git-dumper`, scripts en Python, `netcat`
* **Denegación de Servicio (DoS):** `apachebench` (`ab`), `slowloris`

## 🛡️ Consideraciones de Seguridad (Defense Perspective)
* **Monitoreo:** El tráfico generado desde este host debe ser identificado en el SIEM utilizando el tag `source_host=kali_attacker`.
* **Seguridad:** Mantener las herramientas actualizadas (`apt update && apt upgrade`) y no utilizar credenciales reales dentro del laboratorio.