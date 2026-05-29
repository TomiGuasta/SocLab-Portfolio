# Hallazgos

## Hallazgo 01 — Exposición del servicio SMB

Se identificaron servicios SMB accesibles en:

- TCP 139
- TCP 445

---

## Hallazgo 02 — Sesión SMB anónima habilitada

Fue posible interactuar con SMB sin proporcionar credenciales válidas.

Evidencia:

```bash
smbclient -L //192.168.56.101 -N
```

---

## Hallazgo 03 — Descubrimiento de shares

Se identificaron múltiples recursos SMB compartidos.

Entre ellos, el share **tmp** permitió interacción exitosa.

---

## Hallazgo 04 — Validación de lectura y escritura

La evaluación confirmó:

✔ subida remota de archivos.

✔ descarga remota de archivos.

Evidencia:

```text
putting file text.txt as \text.txt
```

---

## Evaluación de riesgo

En entornos reales, exposiciones equivalentes podrían permitir:

- acceso no autorizado a datos
- modificación de archivos
- reconocimiento interno
- colocación de archivos maliciosos
- exposición de información sensible
