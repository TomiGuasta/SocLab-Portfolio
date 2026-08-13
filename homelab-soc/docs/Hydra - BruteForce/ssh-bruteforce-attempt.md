# Detección: SSH Brute Force

Simulación de un ataque de fuerza bruta contra el servicio SSH de la máquina víctima (Ubuntu Server), ejecutado con Hydra desde Kali Linux, y su correspondiente detección en Splunk.

## 1. Ataque — Hydra

```bash
hydra -l tomi -P /tmp/guastayou.txt ssh://<IP_VICTIMA>
```

Ataque de fuerza bruta contra el usuario `tomi` probando 101 contraseñas de un wordlist propio. Hydra encontró una contraseña válida: **1 of 1 target successfully completed, 1 valid password found**.

![Hydra Brute Force Attack](../../screenshots/Hydra_Brute_Force_Attack.png)

## 2. Detección — Splunk

```spl
index=main sourcetype=linux_secure ("Failed password" OR "Accepted password")
| rex "(?<result>Failed|Accepted) password for (invalid user )?(?<user>\S+) from (?<src_ip>[\d\.]+)"
| table _time, result, src_ip, user
| sort _time
```

La query trae todos los eventos de autenticación SSH del Universal Forwarder de la víctima, extrae el resultado (`Failed`/`Accepted`), la IP de origen y el usuario, y los ordena cronológicamente. Se registraron **114 eventos** en la ventana analizada: una seguidilla de `Failed` para el usuario `tomi` desde la misma IP, hasta el evento final `Accepted` que confirma el login exitoso.

![Splunk Forwarder - Attack Report](../../screenshots/Splunk_Forwarder_-_Attack_Report.png)

## Resultado

| Campo | Valor |
|---|---|
| Usuario objetivo | `tomi` |
| Eventos totales | 114 |
| Resultado | Fuerza bruta exitosa (`Accepted` tras múltiples `Failed`) |
| Sourcetype | `linux_secure` |
