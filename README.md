# Daten vom HeizOel24 MEX auslesen und per MQTT versenden

![Screenshot](https://github.com/ltspicer/iobroker.mex/blob/main/mex.png)

https://www.heizoel24.de/mex

Dieses Script liest die MEX Daten vom HeizOel24 Server und sendet diese per MQTT an ein Smarthome System.

Bedingung ist, dass ein MQTT Broker (Server) auf diesem Smarthome System läuft.

Das Script ist nach zBsp /home/pi zu kopieren.

Die Rechte auf 754 setzen ( chmod 754 mex.py )

Crontab erstellen ( crontab -e ):

0 */3 * * * /home/pi/mex.py # Pfad ggf anpassen!

Weitere Instruktionen sind im Script-Kopf zufinden. Da werden auch die notwendigen Daten wie Logins, IP Adresse, Passwörter usw. eingetragen.

Herzlichen Dank an cpatscheider für seine Unterstützung! ( https://github.com/Secret-Lab-Productions/heizoel24-mex/discussions/2 )

Es gab teilweise Probleme, wenn das mex.py Script auf dem gleichen Host wie das Smarthome System läuft.

Lösung: time.sleep(0.1) in den Zeilen 143, 153 und 165 auskommentieren (# entfernen).

------------------------

This script reads the MEX data from the HeizOel24 server and sends it to a smarthome system via MQTT.

The prerequisite is that an MQTT broker (server) is running on this smarthome system.

The script must be copied to e.g. /home/pi.

Set the rights to 754 ( chmod 754 mex.py )

Create crontab ( crontab -e ):

0 */3 * * * * /home/pi/mex.py # Adjust path if necessary!

Further instructions can be found in the script header. The necessary data such as logins, IP address, passwords etc. are also entered there.

Many thanks to cpatscheider for his support! ( [Secret-Lab-Productions/heizoel24-mex#2](https://github.com/Secret-Lab-Productions/heizoel24-mex/discussions/2) )

There were some problems when the mex.py script runs on the same host as the Smarthome system.

Solution: comment out time.sleep(0.1) in lines 143, 153 and 165 (remove #).
