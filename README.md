# Daten vom Heizoel24 MEX in den ioBroker importieren.

![Screenshot](https://github.com/ltspicer/iobroker.mex/blob/main/mex.png)

Natürlich sind auch andere Smarthome Systeme möglich. Es muss lediglich ein MQTT darauf laufen.

Dieses Script liest die MEX Daten vom Heizoel24 Server und sendet diese per MQTT an den ioBroker.

Die Daten sind im ioBroker unter mqtt/0/MEX zufinden.

Das Script ist nach zBsp /home/pi zu kopieren.

Die Rechte auf 754 setzen ( chmod 754 mex.py )

Crontab erstellen ( crontab -e ):

0 */2 * * * /home/pi/mex.py # Pfad ggf anpassen!

Weitere Instruktionen sind im Script-Kopf zufinden.

Herzlichen Dank an cpatscheider für seine Unterstützung! ( https://github.com/Secret-Lab-Productions/heizoel24-mex/discussions/2 )
