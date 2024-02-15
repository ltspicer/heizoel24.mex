# ioBroker Heizoel24 MEX

Daten vom Heizoel24 MEX im ioBroker

Dieses Script liest die MEX Daten vom Heizoel24 Server und sendet diese per MQTT an den ioBroker.

Die Daten sind im ioBroker unter mqtt/0/MEX zufinden.

Das Script ist nach zBsp /home/pi zu kopieren.

Die Rechte auf 754 setzen ( chmod 754 mex.py )

Crontab erstellen:
0 */2 * * * /home/pi/mex.py # Pfad ggf anpassen!

Weitere Instruktionen sind im Script-Kopf zufinden.

Herzlichen Dank an cpatscheider für seine Unterstützung! ( https://github.com/Secret-Lab-Productions/heizoel24-mex/discussions/2 )
