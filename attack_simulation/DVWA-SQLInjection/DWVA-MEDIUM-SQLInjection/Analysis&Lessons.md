# ANALYSIS_AND_LESSONS.md

# Overview

Este documento resume el análisis técnico, comparativas entre niveles de seguridad, oportunidades de detección y principales aprendizajes obtenidos durante el laboratorio **DVWA SQL Injection — Medium Level**.

El objetivo fue comprender cómo evoluciona una vulnerabilidad SQL Injection cuando se incrementa el nivel defensivo de la aplicación.

---

# Comparative Analysis — LOW vs MEDIUM

## Security Behaviour Comparison

| Feature | LOW | MEDIUM |
|----------|-----|---------|
| Classic Quote Payloads | Works | Partial / Blocked |
| Numeric SQL Injection | Works | Works |
| Boolean-Based SQLi | Works | Works |
| UNION SQLi | Works | Works |
| information_schema Enumeration | Works | Works |
| Input Filtering | None | Partial |
| Payload Adaptation Required | No | Yes |

---

## Defensive Changes Introduced by Medium

DVWA Medium incorpora controles adicionales orientados a reducir la explotación directa mediante payloads tradicionales.

Ejemplo:

Payload clásico:

```sql
'users'
```

En múltiples pruebas, este enfoque mostró comportamiento inconsistente o fallos.

Sin embargo, la lógica SQL seguía siendo alcanzable.

---

## Adaptation Strategy

En lugar de abandonar la explotación, se adaptaron los payloads.

### Numeric Injection

Payload exitoso:

```sql
1 AND 1=1
```

El uso de valores numéricos evitó restricciones asociadas a caracteres especiales.

---

### Hexadecimal Encoding

Se utilizó encoding hexadecimal para evitar quote filtering.

Ejemplo:

Payload tradicional:

```sql
'users'
```

Payload adaptado:

```sql
0x7573657273
```

Resultado:

Bypass exitoso.

Enumeration funcional.

---

## Offensive Learning

El ejercicio demuestra un principio importante en Application Security:

**Incrementar controles parciales no equivale a eliminar la vulnerabilidad.**

El atacante simplemente modifica:

- formato del payload
- encoding utilizado
- lógica empleada
- vector de explotación

---

# Detection Opportunities

Este laboratorio también permite observar posibles indicadores útiles para equipos defensivos.

---

## HTTP Indicators of Compromise

Durante el ataque aparecieron patrones claros.

Ejemplos:

```txt
UNION SELECT
AND 1=1
information_schema
version()
database()
0x7573657273
```

Estos elementos representan indicadores comunes de actividad SQLi.

---

## Query String Artifacts

Ejemplos observables en logs HTTP:

```txt
?id=1 AND 1=1
?id=1 UNION SELECT version(),database()
?id=1 UNION SELECT user,password FROM users
```

Estos patrones son candidatos naturales para:

- SIEM detections
- WAF signatures
- HTTP monitoring
- IDS rules

---

## Database Reconnaissance Indicators

Acceso repetido a:

```txt
information_schema.tables
information_schema.columns
```

puede indicar:

- schema discovery
- enumeration phase
- post-validation reconnaissance

Este comportamiento suele preceder etapas de extracción de datos.

---

## Detection Engineering Ideas

### Candidate Detection Rule — UNION Activity

Buscar:

```txt
UNION SELECT
```

sobre parámetros web.

---

### Candidate Detection Rule — Schema Enumeration

Detectar consultas que incluyan:

```txt
information_schema
```

---

### Candidate Detection Rule — Encoded Payloads

Monitorizar patrones:

```txt
0x[HEX_STRING]
```

dentro de parámetros HTTP.

---

## Blue Team Perspective

Desde una visión defensiva, SQL Injection no siempre aparece como un único payload obvio.

Frecuentemente se observa como:

1. probing inicial
2. boolean testing
3. payload tuning
4. enumeration
5. extraction

Comprender la secuencia completa mejora:

- threat hunting
- alert correlation
- SOC visibility
- incident response

---

# Lessons Learned

---

## Lesson 1 — SQL Injection Evolves With Security Levels

LOW permitió explotación directa.

MEDIUM introdujo restricciones adicionales.

El atacante debió adaptar:

- syntax
- payload structure
- encoding approach

---

## Lesson 2 — Partial Sanitization Is Not Enough

Filtrar caracteres específicos no resolvió la vulnerabilidad.

La lógica SQL continuó siendo explotable mediante:

- numeric injection
- boolean logic
- UNION queries
- hexadecimal encoding

---

## Lesson 3 — Enumeration Enables Structured Compromise

El acceso a `information_schema` permitió transformar una vulnerabilidad simple en una cadena de descubrimiento organizada.

Workflow observado:

```txt
Validation
↓
Enumeration
↓
Schema Discovery
↓
Column Mapping
↓
Credential Extraction
```

---

## Lesson 4 — Credential Exposure Is a Realistic Outcome

La explotación no terminó en visualización de tablas.

Finalizó en:

```txt
Credential Disclosure
```

Esto puede derivar en escenarios reales de:

- Account Takeover
- Password Reuse
- Privilege Escalation
- Lateral Movement

---

## Lesson 5 — Detection Matters

Los ataques SQLi generan artefactos observables.

Un monitoreo adecuado puede detectar:

- payload anomalies
- SQL keywords
- unusual query density
- schema enumeration patterns

La visibilidad defensiva resulta crítica.

---

# Final Technical Assessment

## Vulnerability

```txt
SQL Injection
```

## Attack Category

```txt
Web Application Security
```

## Exploitation Type

```txt
UNION-Based SQL Injection
Boolean SQL Injection
Schema Enumeration
Credential Disclosure
```

## Security Level Evaluated

```txt
DVWA — Medium
```

## Overall Result

**Successful exploitation with defensive adaptation.**

---

# Final Conclusion

DVWA Medium representa una excelente transición entre explotación básica y escenarios más realistas de Web Application Security.

Aunque el entorno incorpora controles adicionales, la vulnerabilidad permaneció explotable mediante adaptación técnica.

El laboratorio reforzó conocimientos de:

- SQL fundamentals
- UNION exploitation
- schema discovery
- payload adaptation
- detection opportunities
- offensive/defensive thinking

Este ejercicio aproxima el workflow observado en tareas reales de:

- Pentesting
- AppSec
- Red Teaming
- SOC Analysis
- Threat Detection
