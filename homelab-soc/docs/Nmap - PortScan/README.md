# Detección: Port Scan (nmap) — 3 niveles de agresividad

Serie de escaneos contra la máquina víctima (Ubuntu Server), de menor a mayor agresividad, intercambiando tambien la velocidad y la cantidad de puertos a analizar para comparar cómo cambia el "rastro" que dejan en los logs y qué tan fácil es detectarlos con la misma query.

### Query Utilizada:
```spl
index=main host=<host-name> sourcetype=linux_secure
("Connection closed" OR "Connection reset" OR "Did not receive identification string")
| table _time, _raw
| sort _time
```

---

## Nivel 1 — Básico

![Nmap Attack](https://raw.githubusercontent.com/TomiGuasta/SocLab-Portfolio/main/homelab-soc/docs/Nmap%20-%20PortScan/Nmap%20-%20Attack.png)

```bash
nmap -sV <IP_VICTIMA>
```

Escanea los primeros 1000 puertos (puertos generales) con detección de versión. Encontró 2 puertos abiertos (22/ssh, 8089/ssl-http).
En este scan se busca la forma mas "burda" que hay de intentar conocer los puertos logicos abiertos, en un sistema operativo. Agregando el parametro -sV para conocer las versiones de los servicios que se alojan en esos puertos.


**Detección en Splunk:** 4 eventos ** — conexiones cortadas antes de autenticación (`[preauth]`, `kex_exchange_identification`).

![Nmap Splunk Report](https://raw.githubusercontent.com/TomiGuasta/SocLab-Portfolio/main/homelab-soc/docs/Nmap%20-%20PortScan/Nmap%20-%20Splunk%20Report.png)

---

## Nivel 2 — Intermedio (todos los puertos, rápido)

![Nmap Attack Lvl 2](https://raw.githubusercontent.com/TomiGuasta/SocLab-Portfolio/main/homelab-soc/docs/Nmap%20-%20PortScan/Nmap%20-%20Attack%20lvl%202.png)

```bash
nmap -sV -sC -A -p- -T4 <IP_VICTIMA>
```

Escaneo de los 65535 puertos, con scripts default (`-sC`) y modo agresivo (`-A`, incluye detección de SO). Ademas de agregarle el aprametro (-T4) que lo que permite es aumentar la velocidad del script , en una escala del 1-5 que dispone Nmap.



**Detección en Splunk:** también 4 eventos, en una ventana similar a la del nivel 1 (~15 segundos). A pesar de escanear 65 veces más puertos que el nivel 1, **la cantidad de eventos detectados no aumentó** — porque solo el puerto 22 (SSH) genera este tipo de log; el resto de los puertos cerrados no dejan rastro en `auth.log`.

![Nmap Splunk Report Lvl 2](https://raw.githubusercontent.com/TomiGuasta/SocLab-Portfolio/main/homelab-soc/docs/Nmap%20-%20PortScan/Nmap%20-%20Splunk%20Report%20lvl%202.png)

---

## Nivel 3 — Agresivo y lento (el más pesado)

![Nmap Attack Lvl 3 T2](https://raw.githubusercontent.com/TomiGuasta/SocLab-Portfolio/main/homelab-soc/docs/Nmap%20-%20PortScan/Nmap%20-%20Attack%20lvl%203%20T2.png)
![Nmap Attack Lvl 3 T4](https://raw.githubusercontent.com/TomiGuasta/SocLab-Portfolio/main/homelab-soc/docs/Nmap%20-%20PortScan/Nmap%20-%20Attack%20lvl%203%20T4.png)

```bash
nmap -sV -sC -A -p- -T2 <IP_VICTIMA>
```

Mismo alcance que el nivel 2 (todos los puertos, scripts, modo agresivo) pero con `-T2`, una velocidad bastante lenta pensada para evadir detección. Se dejó correr **~30 minutos** y se cortó manualmente sin llegar a completar — para esa altura seguía en fase de SYN Stealth Scan(como se puede observar en la imagen documentada del splunk).



**Detección en Splunk: sin resultados.** La misma query que detectó los niveles 1 y 2 no arrojó ningún evento durante los 30 minutos que corrió el escaneo.

### Analisis de los resultados de Splunk a "los tres niveles" de script que se corrieron con Nmap a traves de Kali Linux.

No es que el ataque no haya generado actividad; es que la detección tiene un **punto ciego** frente a este patrón:

- La query solo mira `auth.log` (eventos de SSH). Un escaneo de puertos completo pasa la enorme mayoría del tiempo tocando puertos **sin ningún servicio** corriendo — esos no generan ningún log de aplicación, porque no hay nada escuchando ahí que pueda registrar el intento.
- Con `-T2`, nmap espera deliberadamente entre paquetes. Si en los 30 minutos que corrió todavía no había llegado a tocar el puerto 22, no había nada que la query pudiera encontrar.
- Esto reproduce un problema real de detección: una regla pensada para patrones de ráfaga corta (varios eventos concentrados en pocos segundos) **no está diseñada para cazar actividad lenta y dispersa en el tiempo** — que es exactamente la técnica que un atacante real usaría para evadir un SOC.

---

## Comparación de los tres niveles | Parametros Tecnicos 

| Nivel | Comando | Duración | Puertos | Eventos en Splunk | Detectado |
|---|---|---|---|---|---|
| 1 — Básico | `-sV` | 35.31 seg | Top 1000 | 4 | ✅ Sí |
| 2 — Intermedio | `-sV -sC -A -p- -T4` | ~60 seg | 65535 | 4 | ✅ Sí |
| 3 — Agresivo lento | `-sV -sC -A -p- -T2` | 30+ min (cortado) | 65535 (parcial) | 0 | ❌ No |

## Conclusión

Pude concluir a traves de las tres diferentes simulaciones, que el volumen de puertos escaneados no es lo que determina si un ataque se detecta — lo que importa es si genera **actividad sobre un servicio que efectivamente loguea eventos** (en este caso, SSH) y si esa actividad **cae dentro de la ventana temporal que la detección está mirando**. El nivel 3 demuestra que una detección efectiva contra escaneos rápidos puede ser completamente ciega ante la misma técnica ejecutada más despacio — una limitación real que en un SOC profesional se resolvería correlacionando además con logs de red/firewall (no solo logs de aplicación) y usando ventanas de análisis más largas para detectar patrones de baja frecuencia.
