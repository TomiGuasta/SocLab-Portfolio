# 03 — Brute Force contra el login de DVWA

Ataque de fuerza bruta con Hydra contra el módulo **Brute Force** de DVWA (nivel de seguridad Low), atacando el formulario de login vía HTTP en vez de SSH — mismo objetivo conceptual que el ataque a SSH, pero contra un protocolo sin estructura fija de autenticación.

## Comando base utilizado

```bash
hydra -l admin -P /tmp/guastayou.txt 192.168.0.28 http-get-form \
"/dvwa/vulnerabilities/brute/:username=^USER^&password=^PASS^&Login=Login:F=Username and/or password incorrect" \
-c "PHPSESSID=<valor>; security=low"
```

- `http-get-form` → módulo de Hydra para atacar formularios de login enviados por GET
- `F=Username and/or password incorrect` → texto que Hydra usa para reconocer un intento fallido
- `-c "PHPSESSID=...; security=low"` → cookie de sesión necesaria, porque DVWA requiere una sesión activa para procesar el formulario

Se realizaron **tres intentos** de este ataque, ajustando parámetros entre cada uno para tratar de eliminar los falsos positivos que aparecían en el resultado.

## Intento 1 — Ataque básico

Primer intento, con la wordlist completa (5000 contraseñas + `password` al final) y la cookie de sesión inicial, sin ajustes adicionales.

**Resultado:** Hydra marcó **16 contraseñas como válidas** — un número imposible para un solo usuario con una sola contraseña real, señal clara de falsos positivos.

## Intento 2 — Ajuste de timeout de sesión y concurrencia (`-t`)

Se planteó la hipótesis de que la sesión de DVWA expiraba a mitad del ataque, haciendo que Hydra perdiera de vista el mensaje de error esperado. Se aplicaron dos cambios:

- Se aumentó `session.gc_maxlifetime` a `3600` en `php.ini`, para extender la duración de la sesión
- Se relanzó el ataque probando distintos valores de concurrencia (`-t 1`, `-t 2`, `-t 3`), con una cookie de sesión renovada en cada corrida

**Resultado:** el número de falsos positivos bajó de 16 a un rango de **1 a 4**, pero seguía sin ser el resultado limpio esperado (1 sola contraseña válida). Se observó además un patrón: la cantidad de falsos positivos escalaba junto con el valor de `-t` usado (más threads simultáneos → más falsos positivos), y todos correspondían a las primeras contraseñas del wordlist, no a posiciones aleatorias.

![Hydra - ataques con distintos valores de -t](../../screenshots/hydra-dvwa-brute-attempts.png)

| Threads (`-t`) | Contraseñas marcadas como "válidas" |
|---|---|
| `-t 1` | `123456` |
| `-t 2` | `123456`, `12345` |
| `-t 3` | `12345`, `123456`, `123456789` |

## Intento 3 — Modo debug (`-v -V`)

Para intentar identificar la causa exacta, se relanzó el ataque con `-t 1` y las flags `-v -V`, que muestran en pantalla cada intento y la respuesta del servidor en tiempo real:

```bash
hydra -l admin -P /tmp/guastayou.txt -t 1 -v -V 192.168.0.28 http-get-form \
"/dvwa/vulnerabilities/brute/:username=^USER^&password=^PASS^&Login=Login:F=Username and/or password incorrect" \
-c "PHPSESSID=<valor>; security=low"
```

**Resultado:** con concurrencia mínima (`-t 1`) y visibilidad completa del proceso, Hydra encontró **una sola contraseña válida** — el comportamiento correcto y esperado.

## Verificación manual

Se probó cada contraseña marcada como "válida" en los tres intentos, directamente en el navegador. **Solo `password`** (la contraseña real de `admin` en DVWA) permitió el login efectivamente en todos los casos. El resto (`12345`, `123456`, `123456789`, y las 16 del primer intento) resultaron **falsos positivos**.

## Conclusión de la investigación

El patrón observado entre los tres intentos — el número de falsos positivos cae a medida que baja la concurrencia, hasta desaparecer por completo con `-t 1` — indica que la causa está relacionada con **el manejo de sesión de PHP bajo múltiples requests simultáneos**, no con expiración por tiempo (el ajuste de `session.gc_maxlifetime` no tuvo efecto por sí solo). Con varios threads atacando la misma `PHPSESSID` al mismo tiempo, el servidor parece devolver respuestas inconsistentes en los primeros intentos, antes de estabilizarse — probablemente por cómo PHP bloquea el archivo de sesión ante accesos concurrentes al mismo identificador. No se profundizó más allá de este punto por estar fuera del alcance del ejercicio.

## Por qué se documenta esto igual (y por qué importa)

Este resultado, aunque no sea un ataque "limpio", es un hallazgo válido en sí mismo: demuestra que **las herramientas de ataque automatizado pueden generar falsos positivos**, especialmente contra aplicaciones con manejo de sesión particular (como DVWA con concurrencia HTTP). La lección aplicable a un rol de SOC/analista no es solo "encontrar una alerta", sino **verificar manualmente antes de escalar un hallazgo como confirmado** — un analista que reporta 4 credenciales comprometidas cuando solo 1 es real genera ruido innecesario y erosiona la confianza en sus reportes.

## Detección en Splunk

```spl
index=main sourcetype=access_combined uri="*brute*" clientip=<IP_KALI>
| table _time, method, uri, status
| sort _time
```

A diferencia de SSH (que distingue `Failed password` / `Accepted password` como eventos separados), **HTTP no distingue éxito o fracaso de autenticación a nivel de protocolo** — todos los requests devuelven status `200` (la página siempre carga), haya acertado la contraseña o no. Por eso, para detectar este tipo de ataque en logs web, la señal no está en el `status`, sino en el **volumen de requests a la misma ruta desde la misma IP en poco tiempo** — el mismo principio de detección que se usó para SSH, adaptado a que acá el criterio de "éxito" no es visible en el código de respuesta.

![Detección en Splunk - requests a /brute/](../../screenshots/splunk-dvwa-brute-detection.png)

## Resumen

| Intento | Ajuste aplicado | Falsos positivos |
|---|---|---|
| 1 — Básico | Ninguno | 16 |
| 2 — Timeout + `-t` | `session.gc_maxlifetime=3600`, variando concurrencia | 1 a 4 |
| 3 — Debug | `-t 1` + `-v -V` | 0 |

| Campo | Valor |
|---|---|
| Objetivo | Login de DVWA (`admin`) |
| Herramienta | Hydra (`http-get-form`) |
| Credencial real encontrada | `password` |
| Causa de los falsos positivos | Manejo de sesión de PHP bajo requests concurrentes a la misma `PHPSESSID` |
| Solución efectiva | Reducir concurrencia a `-t 1` |
| Lección clave | Verificar manualmente antes de confirmar un hallazgo de una herramienta automatizada, y no asumir que más velocidad de ataque es siempre mejor |
