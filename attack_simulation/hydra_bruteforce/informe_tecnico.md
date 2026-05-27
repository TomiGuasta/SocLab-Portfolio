# Análisis Técnico Post-Ataque — Hydra  Brute Force

## Resumen Ejecutivo

Se realizó una simulación controlada de ataque de BruteForce
contra el servicio Telnet expuesto por una instancia de Metasploitable 2.

El ejercicio tuvo como objetivo generar telemetría de autenticación,
analizar la evidencia producida y evaluar posibles oportunidades de
detección dentro de un entorno de laboratorio.

Infraestructura utilizada:

Atacante: Kali Linux

Objetivo: Metasploitable 2

Red: VirtualBox Host-Only Network

Servicio atacado:

TCP/23 — Telnet

---

## Descripción del Ataque

Se utilizó la herramienta Hydra para ejecutar un ataque de diccionario
contra el servicio Telnet del sistema objetivo.

Metodología aplicada:

- usuario fijo (`msfadmin`)
- diccionario de contraseñas (`rockyou.txt`)
- múltiples intentos concurrentes
- autenticación repetitiva automatizada

Posteriormente se monitorearon los registros del sistema objetivo para
evaluar el impacto y la evidencia generada.

---

## Evidencia Observada

Durante la simulación se observaron múltiples eventos registrados dentro de:

```text
/var/log/auth.log
```

Patrones identificados:

- intentos fallidos repetitivos de autenticación
- alta frecuencia temporal entre eventos
- reiteración constante de la IP origen
- actividad asociada al servicio Telnet

Ejemplo de evidencia:

```text
FAILED LOGIN
authentication attempts
repeated source host
```

---

## Indicadores de Compromiso (IOC)

Posibles indicadores detectables derivados del ejercicio:

- volumen elevado de autenticaciones fallidas
- múltiples intentos desde un mismo host origen
- actividad anómala sobre servicio Telnet
- comportamiento consistente con credential brute force

---

## Resultado de la Simulación

Hydra logró validar credenciales existentes del sistema objetivo.

Credenciales identificadas:

Usuario:

msfadmin

Contraseña:

msfadmin

---

## Oportunidades de Detección

Posibles mecanismos de detección aplicables:

- detección de fuerza bruta por umbral de intentos fallidos
- correlación de autenticaciones repetidas
- detección basada en frecuencia de eventos
- monitoreo de actividad Telnet
- alertado por abuso de autenticación

---

## Consideraciones Técnicas

Durante las pruebas se identificaron incompatibilidades criptográficas
legacy al intentar ejecutar el ataque sobre SSH.

Como alternativa operacional se utilizó Telnet para completar
la simulación de credential attack dentro del laboratorio.

---

## Aprendizajes Obtenidos

- importancia del análisis de logs de autenticación
- comportamiento observable de ataques automatizados
- diferencias operativas entre servicios legacy
- generación de evidencia útil para workflows SOC / Blue Team
- documentación técnica de incidentes simulados
