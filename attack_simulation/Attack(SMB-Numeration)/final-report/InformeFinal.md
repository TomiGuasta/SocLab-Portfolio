# REPORTE FINAL — SMB ENUMERATION ANALYSIS

## Clasificación

Laboratorio Controlado — Blue Team / SOC Analyst / Security Assessment

---

## Resumen Ejecutivo

Se realizó una evaluación de **enumeración SMB** sobre un entorno vulnerable controlado utilizando **Metasploitable 2** como sistema objetivo y **Kali Linux** como estación atacante.

El ejercicio tuvo como finalidad identificar:

- exposición del servicio SMB
- sesiones anónimas
- descubrimiento de usuarios
- enumeración de shares
- validación de capacidades de lectura y escritura

La evaluación permitió confirmar acceso exitoso sobre un share SMB expuesto y validar operaciones de interacción remota.

---

## Entorno de laboratorio

### Máquina atacante

**Kali Linux**

Herramientas utilizadas:

- Nmap
- NSE SMB Scripts
- enum4linux
- smbclient

### Máquina objetivo

**Metasploitable 2**

Servicios evaluados:

- SMB / Samba
- TCP 139
- TCP 445

---

## Metodología aplicada

La evaluación siguió una secuencia progresiva de reconocimiento y validación.

### 1 — Descubrimiento del servicio

Se verificó disponibilidad del servicio SMB.

Comando utilizado:

```bash
nmap -sV -p139,445 192.168.56.101
```

Objetivo:

- confirmar puertos abiertos
- identificar Samba
- validar superficie inicial de ataque

---

### 2 — Enumeración SMB con Nmap

Se ejecutaron scripts NSE orientados a SMB.

```bash
nmap --script smb-enum-* -p445 192.168.56.101 -oN smb_enum_output.txt
```

Objetivo:

- enumerar shares
- identificar usuarios
- recolectar configuración SMB
- descubrir información del servicio

---

### 3 — Enumeración avanzada con enum4linux

Se realizó enumeración ampliada.

```bash
enum4linux 192.168.56.101 > smb-enum4linux.txt
```

Objetivo:

Obtener información adicional sobre:

- usuarios
- RID cycling
- SID
- password policy
- recursos compartidos

---

### 4 — Validación de sesión SMB anónima

Se verificó interacción sin autenticación.

```bash
smbclient -L //192.168.56.101 -N
```

Resultado observado:

Fue posible listar recursos SMB utilizando sesión anónima.

---

### 5 — Acceso manual a share compartido

Se estableció conexión directa con el share identificado.

```bash
smbclient //192.168.56.101/tmp -N
```

Objetivo:

Validar interacción manual con el recurso compartido.

---

### 6 — Validación de permisos remotos

Se realizó prueba controlada de lectura y escritura.

#### Creación de archivo local

```bash
echo "SMB TEST" > text.txt
```

#### Subida remota

```bash
put text.txt
```

#### Descarga remota

```bash
get text.txt
```

Resultado:

Se confirmaron capacidades exitosas de:

- escritura remota
- lectura remota

---

## Hallazgos principales

### Hallazgo 01 — Servicio SMB expuesto

Se identificaron servicios accesibles en:

- TCP 139
- TCP 445

---

### Hallazgo 02 — Sesiones SMB anónimas habilitadas

La evaluación permitió interacción SMB sin autenticación válida.

Impacto potencial:

- reconnaissance interno
- descubrimiento de shares
- enumeración de usuarios

---

### Hallazgo 03 — Enumeración de usuarios

La evaluación recuperó información sobre cuentas presentes en el sistema.

Ejemplos observados:

- root
- msfadmin
- mysql
- postgres
- www-data

Impacto potencial:

- brute force targeting
- credential attacks
- reconnaissance previo a explotación

---

### Hallazgo 04 — Share accesible

Se identificó un recurso compartido con acceso funcional:

```text
tmp
```

La interacción permitió:

- listar contenido
- acceder al share
- operar sobre archivos

---

### Hallazgo 05 — Validación de lectura y escritura

La prueba manual confirmó:

✔ subida de archivos.

✔ descarga de archivos.

Evidencia observada:

```text
putting file text.txt as \text.txt
```

---

## Perspectiva de seguridad

Aunque el laboratorio utilizó un entorno vulnerable controlado, configuraciones equivalentes en ambientes reales podrían derivar en:

- acceso no autorizado a archivos
- exposición de información sensible
- enumeración interna del entorno
- modificación de contenido compartido
- colocación de archivos no autorizados

Shares equivalentes asociados a:

- backups
- configuraciones
- documentación interna
- scripts administrativos

podrían incrementar significativamente el impacto.

---

## Evidencia recolectada

Outputs generados:

- smb_enum_output.txt
- smb-enum4linux.txt
- smbclient_session.txt

Capturas:

- descubrimiento SMB
- ejecución de enum4linux
- listado de shares
- acceso al share tmp
- validación PUT
- validación GET

---

## Conclusiones

El ejercicio permitió validar exitosamente un flujo completo de **SMB Enumeration y Access Validation**.

Se confirmaron:

✔ descubrimiento del servicio.

✔ enumeración SMB.

✔ acceso anónimo.

✔ acceso a shares.

✔ validación de permisos remotos.

Desde una perspectiva **Blue Team / SOC Analyst**, este escenario demuestra cómo una exposición SMB puede convertirse en una fuente significativa de:

- exposición de datos
- superficie de ataque interna
- recolección de inteligencia operativa
- acceso remoto no autorizado

Medidas defensivas recomendadas:

- deshabilitar sesiones anónimas
- restringir shares innecesarios
- aplicar hardening de Samba
- fortalecer políticas de autenticación
- monitorear actividad SMB
- auditar permisos de recursos compartidos
