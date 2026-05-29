# Análisis de Enumeración SMB — Metasploitable 2

## Objetivo

Realizar un proceso de **enumeración SMB** sobre un entorno vulnerable controlado con el fin de identificar:

- servicios SMB expuestos
- acceso anónimo
- enumeración de usuarios
- descubrimiento de shares
- validación de permisos de lectura y escritura

---

## Entorno de laboratorio

### Máquina atacante

- Kali Linux

### Máquina objetivo

- Metasploitable 2

### Protocolo evaluado

- SMB / Samba

---

## Herramientas utilizadas

- Nmap
- Scripts NSE SMB
- enum4linux
- smbclient

---

## Resultados principales

✔ Descubrimiento del servicio SMB.

✔ Enumeración de usuarios y shares.

✔ Validación de sesión SMB anónima.

✔ Acceso manual a shares compartidos.

✔ Validación de lectura remota.

✔ Validación de escritura remota.

---
