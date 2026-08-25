# DoS contra DVWA (Apache Bench + Slowloris)

Ataque de denegación de servicio contra la web DVWA, combinando dos técnicas distintas: saturación por volumen de requests (Apache Bench) y agotamiento de conexiones (Slowloris), ambas tecnicas son utilizadas mediante SlowLoris. El objetivo acá no es robar información ni descubrir rutas — es dejar el servicio sin capacidad de respuesta, mediante la saturacion de requests o conexiones abiertas.

## Setup Herramientas utilizadas (Kali)

```bash
sudo apt install -y apache2-utils slowloris
```

---

## Ataque 1 — Apache Bench (saturación por volumen)

```bash
ab -n 5000 -c 100 http://192.168.0.28/dvwa/
```
- `-n 5000` → 5000 requests totales
- `-c 100` → 100 requests simultáneos

**Qué pasó:** el volumen de tráfico saturó Apache al punto de dejarlo sin responder. Después de correr el ataque, la web dejó de cargar por completo — ni el navegador ni `curl` obtenían respuesta:

```bash
curl -I http://192.168.0.28/dvwa/
```
(sin respuesta / timeout)

## Diagnóstico y recuperación

Se verificó el estado de los servicios involucrados:

```bash
sudo systemctl status apache2
sudo systemctl status mysql
top
```

Se intentaron varios reinicios de Apache, con resultados inconsistentes al principio (el servicio volvía a quedar no-responsivo poco después de cada restart). Finalmente se optó por un reinicio completo de la máquina:

```bash
sudo reboot
```

Tras el reinicio completo, se confirmó que Apache y MySQL volvían a responder con normalidad.

---

## Ataque 2 — Slowloris (agotamiento de conexiones)

### Primer intento — falló, porque Apache seguía caído del Ataque 1

```bash
slowloris 192.168.0.28 -p 80
```

**Resultado:** `Socket count: 0`. Slowloris no pudo abrir ninguna conexión real, porque Apache todavía no estaba respondiendo tras el Ataque 1 — no había nada que "colgar", las conexiones se rechazaban de entrada.

![Slowloris - primer intento, socket count 0](../../screenshots/slowloris-intento-fallido.png)

### Segundo intento — exitoso, tras recuperar Apache

Con Apache ya funcionando de nuevo (post-reboot), se relanzó el mismo ataque:

```bash
slowloris 192.168.0.28 -p 80
```

**Resultado:** esta vez sí abrió y mantuvo conexiones activas. Se confirmó en tiempo real desde Ubuntu, monitoreando el conteo de conexiones establecidas en el puerto 80:

```bash
watch -n 1 'sudo ss -tan | grep :80 | grep ESTAB | wc -l'
```

El contador subió hasta **150 conexiones simultáneas** — coincidiendo con las 150 sockets que Slowloris reportaba estar manteniendo abiertas del lado del atacante. Mientras el ataque estuvo activo, la web dejó de responder a nuevos visitantes: todos los slots de conexión de Apache estaban ocupados por las conexiones "colgadas" de Slowloris.

---

## Detección en Splunk

### Lo esperado que no funcionó: `access_combined`

```spl
index=main sourcetype=access_combined clientip=192.168.0.36
| timechart span=1s count
```

No mostró nada relevante durante el DoS. Explicación: Apache solo escribe en `access.log` cuando un request **se completa** — ni el volumen de Apache Bench (que sí completa requests, pero el log no diferencia entre carga normal y ataque salvo por el pico de volumen) ni las conexiones incompletas de Slowloris (que nunca terminan) generan el tipo de evento que esta detección esperaba ver con claridad.

### Donde sí apareció evidencia: `apache_error`

```spl
index=main sourcetype=apache_error
| table _time, _raw
| sort _time
```

Reveló una secuencia de **6 reinicios de Apache en aproximadamente 12 minutos** (`caught SIGWINCH, shutting down gracefully` seguido de `resuming normal operations`) — un patrón de caídas y recuperaciones repetidas que no ocurre en operación normal, y que coincide con la ventana de tiempo en la que se ejecutaron los ataques y los reinicios manuales de recuperación.

![Splunk - reinicios repetidos de Apache en apache_error](../../screenshots/splunk-apache-error-restarts.png)

---

## Verificación final — recuperación completa del entorno

```bash
sudo systemctl status apache2
sudo systemctl status mysql
curl -I http://192.168.0.28/dvwa/
```

Todos los servicios confirmados operativos, la web respondiendo con normalidad tras finalizar las pruebas.

---

## Interpretación

Este ataque deja dos lecciones distintas a las de los anteriores:

1. **Un ataque puede fallar por el éxito de otro ataque previo** — Slowloris no pudo ejecutarse correctamente en su primer intento no por un error propio, sino porque Apache Bench ya había dejado el servicio caído. En un escenario real, esto también aplica al revés: un atacante puede necesitar confirmar que el servicio sigue en pie antes de lanzar una segunda técnica.
2. **La detección de un DoS no siempre está donde se esperaría.** El log de accesos (`access_combined`), que fue la fuente principal de detección en los ataques anteriores (fuerza bruta, fuzzing), no mostró nada útil acá. La señal apareció en el log de **errores** del servicio — un recordatorio de que distintos tipos de ataque dejan huella en fuentes de datos distintas, y limitarse a una sola fuente de logs puede dejar puntos ciegos.

## Resumen

| Campo | Valor |
|---|---|
| Herramientas | Apache Bench (`ab`), Slowloris |
| Efecto logrado | Apache no-responsivo, requirió reinicio completo de la máquina |
| Conexiones simultáneas confirmadas (Slowloris) | 150 |
| Detección efectiva | `sourcetype=apache_error` (reinicios repetidos) |
| Detección sin señal | `sourcetype=access_combined` |
| Estado final | Servicios recuperados y verificados operativos |
