1. Instalar Apache en Ubuntu Server
bash
sudo apt update
sudo apt install -y apache2
sudo systemctl enable apache2 --now

Verificár que esté corriendo el servicio Apache:

bash
sudo systemctl status apache2

2. Confirmar servicio Apache - desde Kali Linux
bash
curl http://<IP_UBUNTU>



3. Generar directorios "generales" para posteriormente detectarlos con GoBuster:

bash
sudo mkdir /var/www/html/admin
sudo mkdir /var/www/html/backup
echo "<h1>Panel de administración (prueba)</h1>" | sudo tee /var/www/html/admin/index.html
echo "backup viejo, no debería estar expuesto" | sudo tee /var/www/html/backup/notas.txt

## Serian rutas ocultas que suelen ser las mas buscadas a la hora de atacar con fuzzing un servidor web.

4. Configurar Splunk para mandar los logs de Apache
bash
sudo /opt/splunkforwarder/bin/splunk add monitor /var/log/apache2/access.log -index main -sourcetype access_combined -auth admin:TuPasswordSegura123
sudo /opt/splunkforwarder/bin/splunk add monitor /var/log/apache2/error.log -index main -sourcetype apache_error -auth admin:TuPasswordSegura123
sudo /opt/splunkforwarder/bin/splunk restart
access.log → cada request que llega  — esto detecta el ataque fuzzing
error.log → errores del servidor 



1. Instalar gobuster en Kali (si no lo tenés ya)
bash
sudo apt install -y gobuster

2. Lanzar el escaneo de directorios
bash
gobuster dir -u http://<IP_UBUNTU> -w /usr/share/wordlists/dirb/common.txt
dir → modo de fuzzing de directorios/archivos
-u → la URL objetivo
-w → el wordlist (dirb/common.txt viene instalado por default en Kali)


3. Querie ordenada por tiempo, IP, método utilizado, ubicación del directorio y condición (Encontrada o no)

index=main sourcetype=access_combined
| table _time, clientip, method, uri, status
| sort _time

Filtrado por condición distinto a 404 ("No encontrado") y por IP de Kali Linux como atacante:

index=main sourcetype=access_combined status!=404 clientip=192.168.0.36
| table _time, clientip, method, uri, status
| sort _time
