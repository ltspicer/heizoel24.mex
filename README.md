# Daten vom HeizOel24 MEX im ioBroker nutzen

![Screenshot](https://github.com/ltspicer/iobroker.mex/blob/main/mex.png)

Natürlich sind auch andere Smarthome Systeme möglich. Bedingung ist, dass ein MQTT Broker (Server) darauf läuft.

Dieses Script liest die MEX Daten vom HeizOel24 Server und sendet diese per MQTT an den ioBroker.

Die Daten sind im ioBroker unter mqtt/0/MEX (oder mqtt/1/MEX, je nach Instanz) zufinden.

Das Script ist nach zBsp /home/pi zu kopieren.

Die Rechte auf 754 setzen ( chmod 754 mex.py )

Crontab erstellen ( crontab -e ):

0 */3 * * * /home/pi/mex.py # Pfad ggf anpassen!

Weitere Instruktionen sind im Script-Kopf zufinden.

Das Script kann auch auf dem gleichen Host laufen wie der ioBroker. Bei mir machte dies aber nach einiger Zeit Probleme (mqtt error read econnreset).

Herzlichen Dank an cpatscheider für seine Unterstützung! ( https://github.com/Secret-Lab-Productions/heizoel24-mex/discussions/2 )
