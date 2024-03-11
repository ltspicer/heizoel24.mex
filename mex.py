#!/usr/bin/python3

#######################################################################################################
###################################             V1.3               ####################################
###################################  MEX-Daten per MQTT versenden  ####################################
###################################   (C) 2024 Daniel Luginbühl    ####################################
#######################################################################################################

######################################### WICHTIGE INFOS ##############################################
##################     Im Smarthome System ist ein MQTT Broker zu installieren      ###################
################## ---------------------------------------------------------------- ###################
##################          Falls Raspberry: Alles als User PI ausführen!           ###################
################## ---------------------------------------------------------------- ###################
################## mex.py Script auf Rechte 754 setzen mit:                         ###################
################## chmod 754 mex.py                                                 ###################
################## Dieses Script per Cronjob alle 2 bis 4 Stunden ausführen:        ###################
################## crontab -e                                                       ###################
################## 0 */3 * * * /home/pi/mex.py          # Pfad ggf anpassen!        ###################
################## ---------------------------------------------------------------- ###################
################## Vorgängig zu installieren (auf Host, wo dieses Script läuft):    ###################
##################    pip3 install python3-requests                                 ###################
##################    pip3 install paho-mqtt                                        ###################
##################    pip3 install typing-extensions                                ###################
#######################################################################################################

#######################################################################################################
################################### Hier Einträge anpassen! ###########################################

username = "AAAAA@gmail.com"    # Deine Email Adresse bei HeizOel24
passwort = "BBBBBBBBB"          # Dein Passwort bei HeizOel24

broker_address = "192.168.1.50" # MQTT Broker IP (da wo der MQTT Broker läuft)
mqtt_user = "uuuuuu"            # MQTT User      (im MQTT Broker definiert)
mqtt_pass = "pppppp"            # MQTT Passwort  (im MQTT Broker definiert)

debug = False                   # True = Debug Infos auf die Konsole

#######################################################################################################
#######################################################################################################


import requests
import time
import json
import paho.mqtt.client as mqtt

def mqtt_send(client, topic, wert):
    client.publish("MEX/" + topic, wert)

def login():
    if debug:
        print('Login in...')
    global session_id
    url = "https://api.heizoel24.de/app/api/app/Login"
    newHeaders = {'Content-type': 'application/json'}
    reply = requests.post(url, json = { "Password" : passwort, "Username" : username}, headers=newHeaders)

    return_flag = False
    if reply.status_code == 200:
        if debug:
            print("Login OK")
        reply_json = json.loads(reply.text)
        if reply_json['ResultCode'] == 0:
            session_id = reply_json['SessionId']
            if debug:
                print('Session ID: ' + session_id)
            return_flag = True
        else:
            if debug:
                print('ResultCode nicht 0. Keine Session ID erhalten!')
    else:
        if debug:
            print('Login fehlgeschlagen! Heizoel24 Login Status Code: ' + str(reply.status_code))
    return return_flag

def mex():
    login_status = login()
    if login_status == False:
        return "error"
    if debug:
        print('Refresh sensor data cache...')
    url = 'https://api.heizoel24.de/app/api/app/GetDashboardData/'+ session_id + '/1/1/False'
    reply = requests.get(url)
    if reply.status_code == 200:
        if debug:
            print("Daten wurden empfangen")
        sensor_data = reply
    else:
        if debug:
            print('Heizoel24 GetDashboardData Status Code: ' + str(reply.status_code))
        sensor_data = "error"   # Fehler. Keine Daten empfangen.
    return sensor_data

def main():
    topic1 = ['SensorId', 'IsMain', 'CurrentVolumePercentage', 'CurrentVolume', 'NotifyAtLowLevel', 'NotifyAtAlmostEmptyLevel', 'NotificationsEnabled', 'Usage', 'RemainsUntil', 'MaxVolume', 'ZipCode', 'MexName', 'LastMeasurementTimeStamp', 'LastMeasurementWithDifferentValue', 'BatteryPercentage', 'Battery', 'LitresPerCentimeter', 'LastMeasurementWasSuccessfully', 'SensorTypeId', 'HasMeasurements', 'MeasuredDaysCount', 'LastMeasurementWasTooHigh', 'YearlyOilUsage', 'RemainingDays', 'LastOrderPrice', 'ResultCode', 'ResultMessage']
    topic2 = ['LastOrderPrice', 'PriceComparedToYesterdayPercentage', 'PriceForecastPercentage', 'HasMultipleMexDevices', 'DashboardViewMode', 'ShowComparedToYesterday', 'ShowForecast', 'ResultCode', 'ResultMessage']
    RemainsUntilCombined = ['MonthAndYear', 'RemainsValue', 'RemainsUnit']

    try:
        client = mqtt.Client("mex")
        if debug:
            print("paho-mqtt version < 2.0")
    except:
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "mex")
        if debug:
            print("paho-mqtt version >= 2.0")

    if debug:
        print("---------------------")
        print("client:", client)
        print("---------------------")

    client.username_pw_set(mqtt_user, mqtt_pass)
    client.connect(broker_address)

    daten = mex()
    if daten == "error":
        if debug:
            print("Fehler. Keine Daten empfangen.")
        mqtt_send(client, "Items/DataReceived", False)
        client.disconnect()
        return

    daten = daten.json()

    if debug:
        print()
        print("JSON-Daten:")
        print("===========")
        print()
        print(daten)
        print()
        print("---------------------")
        print()
    for n in range(len(topic2)):
        if debug:
            print(topic2[n] + ":", daten[topic2[n]])
        mqtt_send(client, "PricingForecast/" + topic2[n], daten[topic2[n]])
        #time.sleep(0.1)

    daten = daten["Items"]
    daten = daten[0]

    if debug:
        print("---------------------")
    for n in range(len(topic1)):
        if debug:
            print(topic1[n] + ":", daten[topic1[n]])
        mqtt_send(client, "Items/" + topic1[n], daten[topic1[n]])
        #time.sleep(0.1)
    mqtt_send(client, "Items/DataReceived", True)

    daten3 = daten['RemainsUntilCombined']

    if debug:
        print("---------------------")
        print('RemainsUntilCombined:')
    for n in range(len(RemainsUntilCombined)):
        if debug:
            print(RemainsUntilCombined[n] + ":", daten3[RemainsUntilCombined[n]])
        mqtt_send(client, "RemainsUntilCombined/" + RemainsUntilCombined[n], daten3[RemainsUntilCombined[n]])
        #time.sleep(0.1)

    client.disconnect()

if __name__ == '__main__':
    main()
