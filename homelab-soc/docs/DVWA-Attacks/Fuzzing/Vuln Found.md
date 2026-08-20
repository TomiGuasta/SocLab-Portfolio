Durante el fuzzing de directorios , encontre que la ruta .git/HEAD respondía con status 200 — basicamente la carpeta donde esta el control de versiones se encontraba de forma publica (no deberia estarlo), debido a un error de configuración del propio entorno. 

Explotación

Con la carpeta .git/ accesible, se usó git-dumper para reconstruir el repositorio completo a partir de los objetos internos expuestos:

bash
git-dumper http://<IP_UBUNTU>/dvwa/.git/ /tmp/dvwa-git-dump

La imagen subida al repositorio muestra la reconstrucción exitosa de la carpeta completa — código fuente íntegro de la aplicación (login.php, config/, vulnerabilities/, etc.) y el historial completo de commits, con mensajes y autores originales del proyecto.


Que .git/ quede expuesta no es una vulnerabilidad en si, sino que es un error de despliegue. 

El riesgo concreto:
Se puede reconstruir el código fuente completo, incluso si la carpeta pública solo mostraba una versión compilada o parcial del sitio.
El historial de commits puede contener credenciales, claves de API o configuraciones sensibles que en algún momento se subieron por error y luego se "eliminaron" — pero que siguen existiendo en versiones anteriores del historial, recuperables igual.
No requiere ninguna vulnerabilidad de la aplicación en sí: alcanza con que el servidor sirva archivos estáticos de una carpeta que nunca debió ser pública.
Remediación aplicada

Se opto como medida rapida la eliminacion de la carpeta .git del directorio publico. Verificandose luego con otro scan de gobuster, corroborando que efectivamente no se encuentra alli la carpeta .git .

bash
sudo rm -rf /var/www/html/dvwa/.git


Causa

Tras investigar y consultar se consto de que la causa es que al instalar DVWA se usó git clone directo dentro de la carpeta pública del servidor web (/var/www/html/dvwa). Esto dejó la carpeta de control de versiones .git/ — que nunca debería ser accesible desde el navegador — expuesta como cualquier otro archivo del sitio.
