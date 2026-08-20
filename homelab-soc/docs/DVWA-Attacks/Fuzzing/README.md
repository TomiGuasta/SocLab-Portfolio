# 01 — Ataque Fuzzing contra DVWA (Damn Vulnerable Web Application)

Reconocimiento de la estructura real de la aplicación DVWA usando gobuster, en tres niveles de profundidad, con su correspondiente verificación en Splunk para cada uno.

---

## Paso 1 — Descubrir directorios generales

```bash
gobuster dir -u http://<IP>/dvwa/ -w /usr/share/wordlists/dirb/common.txt
```

Escaneo general contra  DVWA, sin parametros específicos.

**Resultado:** encontró la estructura completa de la aplicación — `config/`, `database/`, `docs/`, `external/`, `tests/`, además de los archivos sueltos `login.php`, `logout.php`, `setup.php`, `about.php`, `robots.txt`, `security.txt`, entre otros. También reveló `.git/HEAD` con status 200.



**Query Splunk:**
```spl
index=main sourcetype=access_combined clientip=<IP_KALI>
| table _time, method, uri, status
| sort _time
```

---

## Paso 2 — Fuzzing con extensiones específicas

```bash
gobuster dir -u http://<IP>/dvwa/ -w /usr/share/wordlists/dirb/common.txt -x php,txt,bak,inc
```

El flag `-x` agrega cada extensión a las palabras del wordlist (`admin.php`, `config.inc`, `backup.bak`, etc.) — mas general y real, porque en una aplicación PHP como DVWA la mayoría del contenido interesante son archivos con extensión, no carpetas sueltas.

**Resultado:** confirmó los mismos archivos `.php` ya vistos (`login.php`, `index.php`, `phpinfo.php`, `setup.php`), sumó `favicon.ico` y `php.ini`, y repitió el hallazgo de `.git/HEAD`. Los archivos `.ht*` (htaccess, htpasswd) devolvieron `403` en todas sus variantes de extensión probadas — confirmando que están protegidos correctamente por Apache.


**Query Splunk:**
```spl
index=main sourcetype=access_combined clientip=<IP_KALI>
| table _time, method, uri, status
| sort _time
```

---

## Paso 3 — Fuzzing dentro de `/vulnerabilities/`

```bash
gobuster dir -u http://<IP>/dvwa/vulnerabilities/ -w /usr/share/wordlists/dirb/common.txt
```

Escaneo dirigido a la carpeta donde viven los módulos vulnerables de DVWA — el objetivo es mapear qué vulnerabilidades están disponibles antes de decidir por dónde atacar, tal como lo haría un atacante real perfilando la superficie de ataque.

**Resultado:** reveló 6 módulos — `api`, `captcha`, `exec`, `fi`, `javascript`, `upload` — todos con status `301` . 



**Query Splunk:**
```spl
index=main sourcetype=access_combined clientip=<IP_KALI> uri="*vulnerabilities*"
| table _time, method, uri, status
| sort _time
```

---

## Resumen del ataque

| Paso | Objetivo | Hallazgo principal |
|---|---|---|
| 1 — General | Mapear directorio raíz | Estructura completa + `.git/HEAD` expuesto |
| 2 — Con extensiones | Encontrar archivos `.php`/`.bak`/`.inc` | Confirma archivos PHP reales, `.ht*` bien protegidos |
| 3 — `/vulnerabilities/` | Mapear módulos de ataque disponibles | 6 de 10 módulos descubiertos con este wordlist |
