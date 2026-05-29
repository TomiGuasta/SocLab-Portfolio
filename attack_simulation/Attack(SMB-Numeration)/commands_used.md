# Comandos utilizados

## 1 — Descubrimiento del servicio SMB

Verificación inicial de puertos SMB expuestos.

```bash
nmap -sV -p139,445 192.168.56.101
```

Objetivo:

Identificar disponibilidad del servicio SMB / Samba.

---

## 2 — Enumeración SMB con Nmap

Ejecución de scripts NSE orientados a SMB.

```bash
nmap --script smb-enum-* -p445 192.168.56.101 -oN smb_enum_output.txt
```

Objetivo:

Recolectar información sobre:

- usuarios
- shares
- sesiones
- configuración SMB
- políticas del sistema

El resultado se guardó para evidencia y documentación.

---

## 3 — Enumeración avanzada con enum4linux

```bash
enum4linux 192.168.56.101 > smb-enum4linux.txt
```

Objetivo:

Realizar enumeración ampliada obteniendo:

- usuarios
- RID cycling
- shares
- SID
- password policy

---

## 4 — Descubrimiento de shares anónimos

Listar recursos SMB accesibles.

```bash
smbclient -L //192.168.56.101 -N
```

Objetivo:

Validar acceso SMB sin autenticación.

---

## 5 — Acceso manual al share

Conexión directa al recurso identificado.

```bash
smbclient //192.168.56.101/tmp -N
```

Objetivo:

Validar acceso manual al share.

---

## 6 — Enumeración del contenido remoto

Listado de archivos presentes en el share.

```bash
ls
```

Objetivo:

Inspeccionar contenido remoto disponible.

---

## 7 — Creación de archivo de prueba local

Generación de un archivo inocuo en Kali.

```bash
echo "SMB TEST" > text.txt
```

Objetivo:

Crear evidencia para prueba de subida.

---

## 8 — Prueba de escritura remota

Subida del archivo al share SMB.

```bash
put text.txt
```

Objetivo:

Validar permisos de escritura.

---

## 9 — Prueba de lectura remota

Descarga del archivo desde el share.

```bash
get text.txt
```

Objetivo:

Validar capacidad de lectura / recuperación remota.
