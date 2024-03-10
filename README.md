# Daten vom HeizOel24 MEX auslesen und per MQTT versenden

![Screenshot](https://github.com/ltspicer/iobroker.mex/blob/main/mex.png)


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
