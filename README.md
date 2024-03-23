## Daten vom HeizOel24 MEX auslesen und per MQTT versenden

![Screenshot](https://github.com/ltspicer/iobroker.mex/blob/main/mex.png)

https://www.heizoel24.de/mex

Dieses Python3 Script liest die MEX Daten vom HeizOel24 Server und sendet diese per MQTT (mosquitto) an ein Smarthome System.

Bedingung ist, dass ein MQTT Broker (Server) auf diesem Smarthome System läuft.

Das Script ist nach zBsp /home/pi zu kopieren.

Die Rechte auf 754 setzen ( chmod 754 mex.py )

Crontab erstellen ( crontab -e ):

0 */3 * * * /home/pi/mex.py # Pfad ggf anpassen!

Weitere Instruktionen sind im Script-Kopf zufinden. Da werden auch die notwendigen Daten wie Logins, IP Adresse, Passwörter usw. eingetragen.

Hier kann auch eine json Datei angefordert werden (CalculatedRemaining.json)

Herzlichen Dank an cpatscheider für seine Unterstützung! ( https://github.com/Secret-Lab-Productions/heizoel24-mex/discussions/2 )

Wenn nur die erste Zeile übermittelt wird (kann vorkommen, wenn zBsp das mex.py Script auf dem gleichen Host wie das Smarthome System läuft), dann DELAY im Scriptkopf auf True setzen.

Es gibt einen MEX Telegram Kanal: https://t.me/mex_heizoel24

#### Falls Debugmodus aktiviert wurde (DEBUG = True), unbedingt nach debuggen wieder zurück setzen (DEBUG = False)!

### Viel Spass beim "Mexen". Feedback ist sehr willkommen!


## Changelog

### V2.4 (2024-03-21)

- MQTT deaktivierbar

### V2.3 (2024-03-20)

- Code gesäubert (pylint)
- Variabeln "items", "pricing_forecast", "remains_until_combined" übersichtlicher definiert

### V2.2 (2024-03-19)

- Nun MEX ID eingabe möglich (bei mehreren Geräten)
- PriceComparedToYesterdayPercentage und PriceForecastPercentage überspringen, wenn "False"

### V2.1 (2024-03-18)

- Retain-Flag hinzugefügt. Thx @derlangemarkus

------------------------
------------------------

This Python3 script reads the MEX data from the HeizOel24 server and sends it to a smarthome system via MQTT (mosquitto).

The prerequisite is that an MQTT broker (server) is running on this smarthome system.

The script must be copied to e.g. /home/pi.

Set the rights to 754 ( chmod 754 mex.py )

Create crontab ( crontab -e ):

0 */3 * * * * /home/pi/mex.py # Adjust path if necessary!

Further instructions can be found in the script header. The necessary data such as logins, IP address, passwords etc. are also entered there.

A json file can also be requested here (CalculatedRemaining.json)

Many thanks to cpatscheider for his support! ( [Secret-Lab-Productions/heizoel24-mex#2](https://github.com/Secret-Lab-Productions/heizoel24-mex/discussions/2) )

If only the first line is transmitted (this can happen e.g. if the mex.py script is running on the same host as the Smarthome system), then set DELAY in the script header to True.

There is a MEX Telegram channel: https://t.me/mex_heizoel24

#### If debug mode has been activated (DEBUG = True), be sure to reset it after debugging (DEBUG = False)!

### Have fun with "Mexiing". Feedback is very welcome!
