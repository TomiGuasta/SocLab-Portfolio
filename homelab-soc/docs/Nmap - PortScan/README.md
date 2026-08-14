# Detección: Port Scan (nmap) — 3 niveles de agresividad

Serie de escaneos contra la máquina víctima (Ubuntu Server), de menor a mayor agresividad, para comparar cómo cambia la firma que dejan en los logs y qué tan fácil es detectarlos con la misma query.

**Query de detección usada en los tres niveles** (sin cambios entre uno y otro):

```spl
index=main host=guasta-home sourcetype=linux_secure
("Connection closed" OR "Connection reset" OR "Did not receive identification string")
| table _time, _raw
| sort _time
```

---

## Nivel 1 — Básico

```bash
nmap -sV <IP_VICTIMA>
```

Solo top 1000 puertos con detección de versión. Encontró 2 puertos abiertos (22/ssh, 8089/ssl-http) en **35.31 segundos**.



**Detección en Splunk:** 4 eventos, todos concentrados en una ventana de **~32 segundos** — conexiones cortadas antes de autenticación (`[preauth]`, `kex_exchange_identification`).



---

## Nivel 2 — Intermedio (todos los puertos, rápido)

```bash
nmap -sV -sC -A -p- -T4 <IP_VICTIMA>
```

Escaneo de los 65535 puertos, con scripts default (`-sC`) y modo agresivo (`-A`, incluye detección de SO). Completado en **~60 segundos** gracias a la velocidad `-T4`.



**Detección en Splunk:** también 4 eventos, en una ventana similar a la del nivel 1 (~15 segundos). A pesar de escanear 65 veces más puertos que el nivel 1, **la cantidad de eventos detectados no aumentó** — porque solo el puerto 22 (SSH) genera este tipo de log; el resto de los puertos cerrados no dejan rastro en `auth.log`.



---

## Nivel 3 — Agresivo y lento (el más pesado)

```bash
nmap -sV -sC -A -p- -T2 <IP_VICTIMA>
```

Mismo alcance que el nivel 2 (todos los puertos, scripts, modo agresivo) pero con `-T2`, una velocidad deliberadamente lenta pensada para evadir detección. Se dejó correr **~30 minutos** y se cortó manualmente sin llegar a completar — para esa altura seguía en fase de SYN Stealth Scan.



**Detección en Splunk: sin resultados.** La misma query que detectó los niveles 1 y 2 no arrojó ningún evento durante los 30 minutos que corrió el escaneo.

### Por qué no se detectó nada — y por qué esto es lo más importante de los tres niveles

No es que el ataque no haya generado actividad; es que la detección tiene un **punto ciego** frente a este patrón:

- La query solo mira `auth.log` (eventos de SSH). Un escaneo de puertos completo pasa la enorme mayoría del tiempo tocando puertos **sin ningún servicio** corriendo — esos no generan ningún log de aplicación, porque no hay nada escuchando ahí que pueda registrar el intento.
- Con `-T2`, nmap espera deliberadamente entre paquetes. Si en los 30 minutos que corrió todavía no había llegado a tocar el puerto 22, no había nada que la query pudiera encontrar.
- Esto reproduce un problema real de detección: una regla pensada para patrones de ráfaga corta (varios eventos concentrados en pocos segundos) **no está diseñada para cazar actividad lenta y dispersa en el tiempo** — que es exactamente la técnica que un atacante real usaría para evadir un SOC.

---

## Comparación de los tres niveles

| Nivel | Comando | Duración | Puertos | Eventos en Splunk | Detectado |
|---|---|---|---|---|---|
| 1 — Básico | `-sV` | 35.31 seg | Top 1000 | 4 | ✅ Sí |
| 2 — Intermedio | `-sV -sC -A -p- -T4` | ~60 seg | 65535 | 4 | ✅ Sí |
| 3 — Agresivo lento | `-sV -sC -A -p- -T2` | 30+ min (cortado) | 65535 (parcial) | 0 | ❌ No |

## Conclusión

El volumen de puertos escaneados no es lo que determina si un ataque se detecta — lo que importa es si genera **actividad sobre un servicio que efectivamente loguea eventos** (en este caso, SSH) y si esa actividad **cae dentro de la ventana temporal que la detección está mirando**. El nivel 3 demuestra que una detección efectiva contra escaneos rápidos puede ser completamente ciega ante la misma técnica ejecutada más despacio — una limitación real que en un SOC profesional se resolvería correlacionando además con logs de red/firewall (no solo logs de aplicación) y usando ventanas de análisis más largas para detectar patrones de baja frecuencia.
