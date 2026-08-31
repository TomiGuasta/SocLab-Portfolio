# SQL Injection contra DVWA 
## + Hashing y Crackeo de credenciales almacenadas.

Ataque en tres etapas contra el módulo SQL Injection de DVWA: bypass de la lógica de consulta, extracción de las credenciales almacenadas en la base de datos, y cracking de los hashes obtenidos.

---

## Setup — DVWA

- **DVWA Security:** Low
- **Módulo:** SQL Injection (`/dvwa/vulnerabilities/sqli/`)
- **Campo vulnerable:** User ID — consulta que busca un usuario por su ID sin sanitizar el input

---

## Etapa 1 — Confirmar el comportamiento normal

Se envía `1` en el campo User ID.

![Normal User ID 1](https://raw.githubusercontent.com/TomiGuasta/SocLab-Portfolio/main/homelab-soc/docs/DVWA-Attacks/SQL%20Injection%20+%20Hashing/SQL%20Injection%20Attack%20-%201.png)

La aplicación devuelve los datos de un único usuario — confirma cómo se comporta la consulta legítima antes de manipularla.

## Etapa 2 — Bypass de la lógica SQL

```sql
1' OR '1'='1
```

La condición `'1'='1'` es siempre verdadera, por lo que la consulta deja de filtrar por un ID específico y devuelve **todos** los usuarios.

![Bypass SQLi](https://raw.githubusercontent.com/TomiGuasta/SocLab-Portfolio/main/homelab-soc/docs/DVWA-Attacks/SQL%20Injection%20+%20Hashing/SQL%20Injection%20Attack%20-%201%27%20OR%20%271%27%3D%271.png)

## Etapa 3 — Extracción de credenciales con UNION SELECT

```sql
' UNION SELECT user, password FROM users-- -
```

`UNION SELECT` combina la consulta original con una nueva que pide explícitamente las columnas `user` y `password` de la tabla `users`. 

![Extracción UNION SELECT](https://raw.githubusercontent.com/TomiGuasta/SocLab-Portfolio/main/homelab-soc/docs/DVWA-Attacks/SQL%20Injection%20+%20Hashing/SQL%20Injection%20Attack%20-%20%27%20UNION%20SELECT%20user,%20password%20FROM%20users--%20-.png)

---

## Etapa 4 — Cracking de los hashes obtenidos

### Comando de cracking (hashcat)

```bash
hashcat -m 0 -a 0 -D 1 /tmp/hashes_dvwa.txt /usr/share/wordlists/rockyou.txt
```

![Hashcat SetUp](https://raw.githubusercontent.com/TomiGuasta/SocLab-Portfolio/main/homelab-soc/docs/DVWA-Attacks/SQL%20Injection%20+%20Hashing/Hashcat%20attack%20-%20SetUp.png)
![Hashcat Report](https://raw.githubusercontent.com/TomiGuasta/SocLab-Portfolio/main/homelab-soc/docs/DVWA-Attacks/SQL%20Injection%20+%20Hashing/Hashcat%20attack%20-%20Report%20.png)

---

## Detección en Splunk

**Query de detección:**

```spl
index=main sourcetype=access_combined uri="*sqli*" clientip=192.168.0.36
| table _time, method, uri, status
| sort _time
```

El payload SQL queda visible directamente en la URL, codificado — una firma reconocible: presencia de comillas simples, palabras clave SQL (`OR`, `UNION`, `SELECT`) y guiones dobles (`-- -`).

![Reporte Splunk SQLi](https://raw.githubusercontent.com/TomiGuasta/SocLab-Portfolio/main/homelab-soc/docs/DVWA-Attacks/SQL%20Injection%20+%20Hashing/Splunk%20Report%20-%20SQL%20Injection%20Attack.png)

---

## Resumen

```
┌───────────────────┬────────────────────────────────────────────────────────┐
│ Campo             │ Valor                                                  │
├───────────────────┼────────────────────────────────────────────────────────┤
│ Vulnerabilidad    │ SQL Injection (input sin sanitizar en parámetro id)    │
│ Técnica           │ Bypass + extracción con UNION SELECT                   │
│ Datos comprometidos│ 4 pares usuario/contraseña (MD5)                       │
│ Herramienta Crack │ hashcat                                                │
│ Severidad         │ Alta — compromiso total                                │
└───────────────────┴────────────────────────────────────────────────────────┘
```
