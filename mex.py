#!/usr/bin/python3

###################################################################################################
#################################             V2.4               ##################################
#################################  MEX-Daten per MQTT versenden  ##################################
#################################   (C) 2024 Daniel Luginbühl    ##################################
###################################################################################################

####################################### WICHTIGE INFOS ############################################
################     Im Smarthome System ist ein MQTT Broker zu installieren      #################
################ ---------------------------------------------------------------- #################
################          Falls Raspberry: Alles als User PI ausführen!           #################
################ ---------------------------------------------------------------- #################
################ mex.py Script auf Rechte 754 setzen mit:                         #################
################ chmod 754 mex.py                                                 #################
################ Dieses Script per Cronjob alle 2 bis 4 Stunden ausführen:        #################
################ crontab -e                                                       #################
################ 0 */3 * * * /home/pi/mex.py          # Pfad ggf anpassen!        #################
################ ---------------------------------------------------------------- #################
################ Vorgängig zu installieren (auf Host, wo dieses Script läuft):    #################
################    pip3 install requests                                         #################
################    pip3 install paho-mqtt                                        #################
################    pip3 install typing-extensions                                #################
###################################################################################################

""" Deine Eintragungen ab hier:"""

###################################################################################################
################################### Hier Einträge anpassen! #######################################

USERNAME = "uuuuu@gmail.com"    # Deine Email Adresse bei HeizOel24
PASSWORD = "ppppppppp"          # Dein Passwort bei HeizOel24
MEX_ID = 1                      # Falls mehrere MEX Geräte, hier ID eintragen (2, 3, 4, ...)

MQTT_ACTIVE = True              # Auf False, wenn nichts MQTT published werden soll
BROKER_ADDRESS = "192.168.1.50" # MQTT Broker IP (da wo der MQTT Broker läuft)
MQTT_USER = "xxxxxx"            # MQTT User      (im MQTT Broker definiert)
MQTT_PASS = "yyyyyy"            # MQTT Passwort  (im MQTT Broker definiert)
MQTT_PORT = 1883                # MQTT Port      (default: 1883)

LESS_DATA = True                # Weniger Zukunftsdaten abrufen (nur alle 14 Tage)
CREATE_JSON = True              # True, wenn CalculatedRemaining.json erstellt werden soll
JSON_PATH = ""                  # Pfad für die Json Datei. Standardpfad ist bei Script.
                                # sonst zBsp.: JSON_PATH = "/home/pi/"

DELAY = False                   # Auf True setzen, wenn der MQTT Broker nur die 1. Zeile empfängt
DEBUG = False                   # True = Debug Infos auf die Konsole.
                                # Unbedingt nach debuggen zurück setzen!!
                                # Be sure to reset after debugging!!

###################################################################################################
###################################################################################################

#--------------------------------- Ab hier nichts mehr verändern! --------------------------------#

import time
import json
import random
import requests
import paho.mqtt.client as mqtt

# Zufällige Zeitverzögerung 0 bis 3540 Sekunden (0-59min)
verzoegerung = random.randint(0,3540)
if DEBUG:
    verzoegerung = random.randint(0,5)
print("Datenabfrage startet in", verzoegerung, "Sekunden")
time.sleep(verzoegerung)

def send_mqtt(client, topic, wert):
    """Send MQTT"""
    client.publish("MEX/" + str(MEX_ID) + "/" + topic, wert, 0, True)

def login():
    """Login to Heizoel24 server"""
    if DEBUG:
        print("Login in...")
    url = "https://api.heizoel24.de/app/api/app/Login"
    new_headers = {"Content-type": "application/json"}
    reply = requests.post(
        url, json = { "Password" : PASSWORD, "Username" : USERNAME}, headers=new_headers, timeout=5
    )

    return_flag = False
    if reply.status_code == 200:
        if DEBUG:
            print("Login OK")
        reply_json = json.loads(reply.text)
        if reply_json["ResultCode"] == 0:
            session_id = reply_json["SessionId"]
            if DEBUG:
                print("Session ID: " + session_id)
            return_flag = True
        else:
            if DEBUG:
                print("ResultCode nicht 0. Keine Session ID erhalten!")
    else:
        if DEBUG:
            print("Login fehlgeschlagen! Heizoel24 Login Status Code: " + str(reply.status_code))
    return return_flag, session_id

def mex():
    """MEX Daten holen"""
    login_status, session_id = login()
    if not login_status:
        return "error"
    if DEBUG:
        print("Refresh sensor data cache...")
    url = "https://api.heizoel24.de/app/api/app/GetDashboardData/"\
          + session_id + "/1/" + str(MEX_ID) + "/False"
    reply = requests.get(url, timeout=5)
    if reply.status_code == 200:
        if DEBUG:
            print("MEX ID:", MEX_ID)
            print("Daten wurden empfangen")
        sensor_data = reply
    else:
        if DEBUG:
            print("Heizoel24 GetDashboardData > Status Code: " + str(reply.status_code))
        sensor_data = "error"   # Fehler. Keine Daten empfangen.
    return sensor_data, session_id

def measurement(sensor_id, session_id):
    """Berechnete zukünftige Oelstände holen"""
    if DEBUG:
        print("Hole zukünftige Oelstände...")
    url = "https://api.heizoel24.de/app/api/app/measurement/CalculateRemaining/"\
          + session_id + "/" + str(sensor_id) + "/False"
    reply = requests.get(url, timeout=5)
    if reply.status_code == 200:
        if DEBUG:
            print("Berechnete zukünftige Oelstände wurden empfangen")
        zukunfts_daten = reply
    else:
        if DEBUG:
            print("Heizoel24 Oelstände > Status Code: " + str(reply.status_code))
        zukunfts_daten = "error"   # Fehler. Keine Daten empfangen.
    return zukunfts_daten

def main():
    """Hauptroutine"""
    items = [
        "SensorId",                 "IsMain",                           "CurrentVolumePercentage",
        "CurrentVolume",            "NotifyAtLowLevel",                 "NotifyAtAlmostEmptyLevel",
        "NotificationsEnabled",     "Usage",                            "RemainsUntil",
        "MaxVolume",                "ZipCode",                          "MexName",
        "LastMeasurementTimeStamp", "LastMeasurementWithDifferentValue","BatteryPercentage",
        "Battery",                  "LitresPerCentimeter",        "LastMeasurementWasSuccessfully",
        "SensorTypeId",             "HasMeasurements",                  "MeasuredDaysCount",
        "LastMeasurementWasTooHigh","YearlyOilUsage",                   "RemainingDays",
        "LastOrderPrice",           "ResultCode",                       "ResultMessage"
    ]
    pricing_forecast = [
        "LastOrderPrice",          "PriceComparedToYesterdayPercentage","PriceForecastPercentage",
        "HasMultipleMexDevices",   "DashboardViewMode",                 "ShowComparedToYesterday",
        "ShowForecast",            "ResultCode",                        "ResultMessage"
    ]
    remains_until_combined = [
        "MonthAndYear",            "RemainsValue",                      "RemainsUnit"
    ]

    if DEBUG:
        print("------------------------")
    if MQTT_ACTIVE:
        try:
            client = mqtt.Client("mex")
            if DEBUG:
                print("paho-mqtt version < 2.0")
        except ValueError:
            client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "mex")
            if DEBUG:
                print("paho-mqtt version >= 2.0")

    if DEBUG:
        print("------------------------")

    if MQTT_ACTIVE:
        client.username_pw_set(MQTT_USER, MQTT_PASS)
        try:
            client.connect(BROKER_ADDRESS, port=MQTT_PORT)
        except OSError as error:
            print("Verbindung zum MQTT-Broker fehlgeschlagen")
            print("Connection to MQTT broker failed")
            print(error)
            exit(1)

    daten, session_id = mex()
    if daten == "error":
        if DEBUG:
            print("Fehler. Keine Daten empfangen.")
        if MQTT_ACTIVE:
            send_mqtt(client, "Items/DataReceived", False)
            client.disconnect()
        return

    daten = daten.json()

    if DEBUG:
        print()
        print("JSON-Daten:")
        print("===========")
        print()
        print(daten)
        print()
        print("---------------------")
        print()
    for n, pricing_forecast in enumerate(pricing_forecast):
        if DEBUG:
            print(pricing_forecast + ":", daten[pricing_forecast])
        if (daten[pricing_forecast] is False) and (
            pricing_forecast == "PriceComparedToYesterdayPercentage" or
            pricing_forecast == "PriceForecastPercentage"):
            if DEBUG:
                print(pricing_forecast, "übersprungen weil 'False'")
        else:
            if MQTT_ACTIVE:
                send_mqtt(client, "PricingForecast/" + pricing_forecast, daten[pricing_forecast])
        if DELAY:
            time.sleep(0.05)

    daten = daten["Items"]
    daten = daten[0]

    if DEBUG:
        print("---------------------")
    for n, items in enumerate(items):
        if DEBUG:
            print(items + ":", daten[items])
        if MQTT_ACTIVE:
            send_mqtt(client, "Items/" + items, daten[items])
        if DELAY:
            time.sleep(0.05)
    if MQTT_ACTIVE:
        send_mqtt(client, "Items/DataReceived", True)

    sensor_id = daten["SensorId"]

    daten3 = daten["RemainsUntilCombined"]

    if DEBUG:
        print("---------------------")
        print("RemainsUntilCombined:")
    for n, remains_until_combined in enumerate(remains_until_combined):
        if DEBUG:
            print(remains_until_combined + ":", daten3[remains_until_combined])
        if MQTT_ACTIVE:
            send_mqtt(client, "RemainsUntilCombined/" + remains_until_combined,
                      daten3[remains_until_combined])
        if DELAY:
            time.sleep(0.05)

    zukunfts_daten = measurement(sensor_id, session_id)

    if zukunfts_daten == "error":
        if DEBUG:
            print("Fehler. Keine Daten empfangen.")
            return

    zukunfts_daten = zukunfts_daten.json()

    if CREATE_JSON:
        json_object = json.dumps(zukunfts_daten, indent=4)
        with open(JSON_PATH + "CalculatedRemaining.json","w", encoding="utf-8") as datei:
            datei.write(json_object)

    zukunfts_daten = zukunfts_daten["ConsumptionCurveResult"]

    n = 0
    for key in zukunfts_daten:
        ausfuehren = True
        if LESS_DATA:
            ausfuehren = n % 14 == 0
        if ausfuehren:
            if DEBUG:
                print(key.split("T")[0], zukunfts_daten[key], "Liter remaining")
            if MQTT_ACTIVE:
                send_mqtt(client, "CalculatedRemaining/Today_plus_" + str(n).zfill(4) +
                          "_Days", str(key).split("T", maxsplit=1)[0]\
                          + " = " + str(zukunfts_daten[key]) + " Ltr.")
        n+=1
        if DELAY:
            time.sleep(0.05)
    if MQTT_ACTIVE:
        client.disconnect()

if __name__ == "__main__":
    main()
