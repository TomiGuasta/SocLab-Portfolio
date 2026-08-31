# DoS contra DVWA (Apache Bench + Slowloris)

Ataque de denegación de servicio contra la web DVWA, combinando dos técnicas distintas: saturación por volumen de requests (Apache Bench) y agotamiento de conexiones (Slowloris).

---

## Ataque 1 — Apache Bench (saturación por volumen)

```bash
ab -n 5000 -c 100 http://192.168.0.28/dvwa/
```
- `-n 5000` → 5000 requests totales
- `-c 100` → 100 requests simultáneos

![Ejecución Apache Bench](https://raw.githubusercontent.com/TomiGuasta/SocLab-Portfolio/main/homelab-soc/docs/DVWA-Attacks/DoS/DoS%20Attack%20-%20Apache%20Bench.png)

**Qué pasó:** el volumen de tráfico saturó Apache al punto de dejarlo sin responder. Después de correr el ataque, la web dejó de cargar por completo.

## Diagnóstico y recuperación

Se verificó el estado de los servicios involucrados:

```bash
sudo systemctl status apache2
sudo systemctl status mysql
top
```

Tras varios intentos de reinicio, se optó por un reinicio completo de la máquina:

```bash
sudo reboot
```

---

## Ataque 2 — Slowloris (agotamiento de conexiones)

### Segundo intento (exitoso, tras recuperar Apache)

```bash
slowloris 192.168.0.28 -p 80
```

![Ejecución Slowloris](https://raw.githubusercontent.com/TomiGuasta/SocLab-Portfolio/main/homelab-soc/docs/DVWA-Attacks/DoS/DoS%20Attack%20-%20SlowLoris.png)

**Resultado:** Se confirmó en tiempo real desde Ubuntu, monitoreando el conteo de conexiones establecidas en el puerto 80:

```bash
watch -n 1 'sudo ss -tan | grep :80 | grep ESTAB | wc -l'
```

El contador subió hasta **150 conexiones simultáneas** — todos los slots de conexión de Apache estaban ocupados por las conexiones "colgadas" de Slowloris.

---

## Detección en Splunk

### Evidencia: `apache_error`

```spl
index=main sourcetype=apache_error
| table _time, _raw
| sort _time
```

Reveló una secuencia de **6 reinicios de Apache en aproximadamente 12 minutos**, coincidiendo con la ventana de tiempo de los ataques.

1. **Apache Bench:** Saturación e impacto en disponibilidad.
![Splunk Apache Bench](https://raw.githubusercontent.com/TomiGuasta/SocLab-Portfolio/main/homelab-soc/docs/DVWA-Attacks/DoS/Splunk%20DoS%20Attack%20-%20Apache%20Bench.png)
![Timeline Apache Bench](https://raw.githubusercontent.com/TomiGuasta/SocLab-Portfolio/main/homelab-soc/docs/DVWA-Attacks/DoS/Splunk%20DoS%20Attack%20-%20Apache%20Bench%20TimeLine.png)

2. **Slowloris:** Agotamiento de recursos de Apache.
![Splunk Slowloris](https://raw.githubusercontent.com/TomiGuasta/SocLab-Portfolio/main/homelab-soc/docs/DVWA-Attacks/DoS/Splunk%20DoS%20Attack%20-%20SlowLoris.png)

---

## Resumen del ataque

```
┌───────────────────────────────────────┬─────────────────────────────────────────────────────────┐
│ Campo                                 │ Valor                                                   │
├───────────────────────────────────────┼─────────────────────────────────────────────────────────┤
│ Herramientas                          │ Apache Bench (ab), Slowloris                            │
│ Efecto logrado                        │ Apache no-responsivo, requirió reinicio de la máquina   │
│ Conexiones simultáneas (Slowloris)    │ 150                                                     │
│ Detección efectiva                    │ sourcetype=apache_error (reinicios repetidos)           │
│ Detección sin señal                   │ sourcetype=access_combined                              │
│ Estado final                          │ Servicios recuperados y verificados operativos          │
└───────────────────────────────────────┴─────────────────────────────────────────────────────────┘
```
