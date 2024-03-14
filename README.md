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

Wenn nur die erste Zeile übermittelt wird (kann vorkommen, wenn das mex.py Script auf dem gleichen Host wie das Smarthome System läuft), dann delay im Scriptkopf auf True setzen.

#### Wenn Debugmodus aktiviert wurde (debug = True), unbedingt nach debuggen wieder zurück setzen (debug = False)!

------------------------

This script reads the MEX data from the HeizOel24 server and sends it to a smarthome system via MQTT.

The prerequisite is that an MQTT broker (server) is running on this smarthome system.

The script must be copied to e.g. /home/pi.

Set the rights to 754 ( chmod 754 mex.py )

Create crontab ( crontab -e ):

0 */3 * * * * /home/pi/mex.py # Adjust path if necessary!

Adjust the minute (here 0 in the example) to a random value from 0 to 59 so that not everyone accesses the server at the same time!

Further instructions can be found in the script header. The necessary data such as logins, IP address, passwords etc. are also entered there.

Many thanks to cpatscheider for his support! ( [Secret-Lab-Productions/heizoel24-mex#2](https://github.com/Secret-Lab-Productions/heizoel24-mex/discussions/2) )

If only the first line is transmitted (this can happen if the mex.py script is running on the same host as the Smarthome system), then set delay in the script header to True.

#### If debug mode has been activated (debug = True), be sure to reset it after debugging (debug = False)!
