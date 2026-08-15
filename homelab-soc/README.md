# SOC Lab — Ataque y Detección en Entorno Controlado

## Sobre este proyecto

Este repositorio documenta un laboratorio casero que armé para profundizar mis conocimientos como **SOC Analyst**, combinando una perspectiva ofensiva (Red Team) con el enfoque defensivo que es el foco principal del proyecto (Blue Team).

La idea es  generar actividad maliciosa real en un entorno controlado, utilizando diferentes herramientas y metodos que brinda Kali Linux, observar cómo esa actividad queda registrada en los logs, y construir sobre eso las herramientas que un analista SOC usa en el día a día — queries de búsqueda, reglas de detección y alertas automáticas, de a poco ir armando un playbook con todo lo utilizado en el lab que me sirva para el dia de mañana poder poner a prueba mis conocimientos en un entorno profesional.

No es un curso ni una guía teórica. Es el registro de un proceso de aprendizaje activo: cada componente de este lab lo instalé, rompí, diagnostiqué y volví a levantar yo mismo, y ese proceso de troubleshooting es, en gran parte, tan valioso como el resultado final.

## Objetivo

- Entender de punta a punta el flujo de datos en un SIEM (SPLUNK): desde que un evento ocurre, hasta que un analista lo detecta y actúa sobre él.
- Practicar la mentalidad ofensiva lo justo y necesario para saber qué señales deja un atacante — no para explotar en profundidad, sino para reconocer patrones desde el lado defensivo. Basicamente pensar como atacante para poder implementar la defensa que requiera el sistema.
- Desarrollar la habilidad de escribir queries SPL, reglas de auditoría y alertas propias, en vez de depender solo de detecciones prearmadas. Paralelamente ir guardando esas queries, reglas y alertas para poder armar una especie de playbook, e ir familiarizandome con los conceptos mas generales para poder adaptarlos en diferentes escenarios.
- Construir una base de conocimiento y un repositorio de detecciones reutilizable para cuando me toque aplicar esto profesionalmente.

## Arquitectura del lab

El entorno está armado con tres máquinas conectadas a la misma red local (mismo router, combinando WiFi y ethernet):

```
┌─────────────────────┐         ┌──────────────────────┐
│   Kali Linux (VM)    │ ataca  │   Ubuntu Server        │
│   Atacante            │ ──────▶│   (víctima)            │
│   nmap, hydra, etc.   │        │   SSH, auditd, rsyslog │
└─────────────────────┘         └──────────┬────────────┘
                                             │ Splunk Universal
                                             │ Forwarder (puerto 9997)
                                             ▼
                                  ┌──────────────────────┐
                                  │  PC principal          │
                                  │  Splunk Enterprise      │
                                  │  (indexer + búsquedas   │
                                  │   + alertas por mail)   │
                                  └──────────────────────┘
```

**Kali Linux** corre como VM en modo Bridged, para tomar IP directa de la red local y poder atacar a la víctima como si fuera un actor externo en la misma red.

**Ubuntu Server** es la máquina víctima — una laptop dedicada, con SSH habilitado como superficie de ataque principal, `auditd` configurado con reglas propias para detectar cambios críticos del sistema, y el Splunk Universal Forwarder mandando los logs relevantes al indexer.

**PC principal (Windows)** corre Splunk Enterprise, actuando como el servidor central donde se reciben, indexan y analizan todos los eventos, y desde donde se configuran las alertas.

## Qué se está monitoreando

- `/var/log/auth.log` — autenticación, intentos SSH, uso de sudo
- `/var/log/syslog` — actividad general del sistema
- `/var/log/audit/audit.log` — eventos de auditd según reglas propias (cambios en `/etc/passwd`, `/etc/shadow`, `/etc/sudoers`, ejecución de comandos, cambios en configuración SSH)


## Metodología

El trabajo se organiza en ciclos por cada tipo de ataque:

1. **Ejecutar el ataque** desde Kali (reconocimiento, fuerza bruta, escalada de privilegios, persistencia, etc.)
2. **Observar la señal cruda** que ese ataque deja en los logs de la víctima
3. **Construir la query SPL** que permite encontrar y filtrar esa actividad en Splunk
4. **Convertir la query en una detección/alerta** que dispare automáticamente ante ese patrón
5. **Documentar** el ataque, la detección y los aprendizajes en este repositorio


## Ataques cubiertos (en progreso)

- [x] Reconocimiento con `nmap` (escaneo de puertos y servicios)
- [x] Fuerza bruta SSH con `hydra`
- [ ] Escalada de privilegios local
- [ ] Persistencia (usuarios, cron jobs, claves SSH)
- [ ] Movimiento lateral
- [ ] Exfiltración de datos simulada

Esta lista se va a ir ampliando a medida que el lab crece.


## Aprendizajes y troubleshooting

Parte del valor de este proyecto estuvo en resolver problemas reales de configuración, muy similares a los que aparecen en un entorno de trabajo real:

- Configuración de red mixta (WiFi + ethernet) sobre el mismo router para simular endpoints heterogéneos
- Construir el setup de Ubuntu Server desde cero, desde la instalacion de su SO hasta las configuraciones para permitir Splunk Enterprise, poder habilitar servicios para su explotacion (controladamente), y realizar diferentes modificaciones para poder utilizar a favor del atacante para posteriormente documentarlas.
- Errores de `illegal instruction` por incompatibilidad de instrucciones AVX entre la CPU del lab y binarios recientes de Splunk, resuelto usando una versión anterior
- Diferencia entre `sourcetype` como etiqueta y las extracciones de campo reales — y por qué un Technology Add-on (TA) es necesario para que el parseo automático funcione
- Instalación manual de un TA cuando la vía de instalación web no está disponible por restricciones de licencia

## Próximos pasos

- Sumar más escenarios de ataque y sus detecciones correspondientes
- Explorar dashboards en Splunk para visualizar la actividad del lab de forma más clara
- Evaluar sumar un segundo endpoint (por ejemplo, un Windows Server) para practicar detecciones sobre otra plataforma

---

*Este es un proyecto personal de aprendizaje. Todas las máquinas involucradas son de mi propiedad y están aisladas para fines exclusivamente educativos.*
