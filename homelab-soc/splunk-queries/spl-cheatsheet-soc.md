# Playbook: Comandos SPL comunes para SOC Analyst

Referencia rápida de búsquedas en Splunk (SPL) organizadas por tipo de investigación.

---

## Búsquedas básicas / estructura general

```spl
index=main
```
Trae todos los eventos del índice. Punto de partida para explorar qué está llegando.

```spl
index=main sourcetype=linux_secure
```
Filtra por tipo de log específico (auth.log parseado por Splunk).

```spl
index=main host=ubuntu-victima
```
Filtra por máquina de origen — clave cuando tenés varios endpoints reportando al mismo índice.

```spl
index=main earliest=-24h latest=now
```
Filtra por ventana de tiempo (últimas 24hs). También se puede setear en el selector visual arriba a la derecha.

---

## Autenticación / accesos

```spl
index=main "Failed password"
```
Intentos de login fallidos (SSH). Base para detectar fuerza bruta.

```spl
index=main "Failed password" | stats count by src_ip
| sort -count
```
Cuenta cuántos intentos fallidos hizo cada IP — si una IP tiene cientos de intentos, es fuerza bruta.

```spl
index=main "Accepted password" OR "Accepted publickey"
```
Logins exitosos — cruzar con la búsqueda anterior te dice si una fuerza bruta *terminó* logrando entrar.

```spl
index=main "Failed password" | stats count by user
| sort -count
```
Qué usuarios están siendo atacados (root, admin, usuarios comunes, etc.)

```spl
index=main "session opened" OR "session closed"
```
Apertura/cierre de sesiones — útil para reconstruir cuánto tiempo estuvo alguien conectado.

---

## Escalada de privilegios / sudo

```spl
index=main "sudo:" 
```
Todo uso de sudo — quién, cuándo, qué comando.

```spl
index=main sudo COMMAND
| table _time, user, COMMAND
```
Tabla limpia de comandos ejecutados con sudo (requiere que el campo esté parseado; si no, usar rex).

```spl
index=main "authentication failure" sudo
```
Intentos fallidos de usar sudo (contraseña incorrecta al elevar privilegios).

---

## Auditd (cambios críticos del sistema)

```spl
index=main key=passwd_changes
```
Cambios en `/etc/passwd` — posible creación de usuario para persistencia.

```spl
index=main key=shadow_changes
```
Cambios en `/etc/shadow` — modificación de contraseñas fuera del flujo normal.

```spl
index=main key=sudoers_changes
```
Cambios en `/etc/sudoers` — señal crítica, alguien se está dando privilegios permanentes.

```spl
index=main key=command_execution
| table _time, user, comm, exe
```
Todos los comandos ejecutados en el sistema (regla execve) — reconstrucción de línea de tiempo del atacante.

```spl
index=main key=sshd_config_changes
```
Cambios en la configuración de SSH — posible backdoor (habilitar root login, agregar clave pública).

---

## Red / conexiones

```spl
index=main sourcetype=syslog "Connection from"
```
Conexiones entrantes registradas por syslog/sshd.

```spl
index=main src_ip=<IP_SOSPECHOSA>
```
Todo lo relacionado a una IP puntual — para investigar un origen específico una vez identificado.

```spl
index=main | stats count by src_ip, dest_port
| sort -count
```
Panorama general de qué IPs están tocando qué puertos — útil para detectar escaneos (nmap).

---

## Estadísticas y patrones generales

```spl
index=main | stats count by sourcetype
```
Qué tipos de log están llegando y en qué volumen — buen chequeo de salud del pipeline.

```spl
index=main | timechart count by sourcetype
```
Gráfico de volumen de eventos en el tiempo — detecta picos anómalos de actividad.

```spl
index=main | stats count by host
```
Cuántos eventos manda cada máquina — si tenés varios endpoints, ver cuál genera más ruido.

```spl
index=main | top limit=10 user
```
Los 10 usuarios con más actividad registrada.

---

## Comandos SPL de utilidad general (no filtros, sino transformación)

| Comando | Para qué sirve |
|---|---|
| `stats count by campo` | Cuenta ocurrencias agrupadas por un campo |
| `timechart count` | Serie temporal de eventos (para gráficos) |
| `table campo1, campo2` | Muestra solo columnas específicas, más legible |
| `sort -count` | Ordena de mayor a menor (usar `+` para ascendente) |
| `top limit=N campo` | Los N valores más frecuentes de un campo |
| `rare campo` | Los valores MENOS frecuentes — útil para detectar anomalías/outliers |
| `dedup campo` | Elimina duplicados basados en un campo |
| `rex field=_raw "regex"` | Extrae un campo nuevo con expresión regular, si Splunk no lo parseó solo |
| `eval nuevo_campo=condición` | Crea un campo calculado o condicional |
| `where condición` | Filtra resultados después de un stats/eval (SPL no permite filtrar por campos calculados con solo `search`) |

---

## Notas de uso

- Los nombres exactos de campo (`src_ip`, `user`, `key`, etc.) dependen de cómo Splunk parseó cada sourcetype. Si una búsqueda no devuelve nada, primero corré `index=main` sin filtros y mirá qué campos aparecen en el panel izquierdo ("Interesting Fields").
- Las claves de auditd (`key=passwd_changes`, etc.) son las que definimos nosotros mismos en `/etc/audit/rules.d/lab-soc.rules` — en un entorno real, revisar qué keys están configuradas antes de buscar por ellas.
- `earliest`/`latest` también se pueden escribir como `earliest=-1h`, `-7d`, `-30m`, etc.

---

*Actualizar este archivo a medida que se van descubriendo nuevas queries útiles durante las prácticas.*
