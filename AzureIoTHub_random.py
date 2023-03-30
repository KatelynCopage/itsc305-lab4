#! /usr/bin/env python3

# Created by Lubos Kuzma, School of ICT, SAIT
# Nov, 2021
# Program sends random integers to IoT Hub


                                  #SPI library for communicating with ADC
from time import sleep, process_time            #process_time is used for delays. Counts the running time of process
from gpiozero import Button, LED                #button and LED - digital I/Os
from paho.mqtt import client as mqtt
import ssl
import re                                       #RegEx
from random import randint


#IoT settings
#deviceConnectionString = 'HostName=TestHubICTS305.azure-devices.net;DeviceId=RPiIoT;SharedAccessKey=FWLuNxU4k1KTNaZqx0cU3G7lSkBDbh8P6iJLuik4n7o='

path_to_root_cert = "./AzureBaltimore.cer"                            #<local path to digicert.cer file>"
device_id = "raspberry"
sas_token = "SharedAccessSignature sr=Lab5.azure-devices.net%2Fdevices%2Fraspberry&sig=KOd2yOwmHqxxtzlDIeUzxjCsz6sTDuGcxBQTYHJYAXM%3D&se=1637799298"
iot_hub_name = "Lab5"


def on_connect(client, userdata, flags, rc):
    print("Device connected with result code: " + str(rc))


def on_disconnect(client, userdata, rc):
    print("Device disconnected with result code: " + str(rc))


def on_publish(client, userdata, mid):
    print("Device sent message: ", userdata)

def on_message(client, userdata, message):
    print("Received message:", str(message.payload), " on topic ", str(message.topic))
    
def on_subscribe(client, userdata, mid, granted_qos):
    print("Client subscribed")
    
def on_unsubscribe(client, userdata, mid):
    print("Client Unsubscribed")


azureClient = mqtt.Client(client_id=device_id, protocol=mqtt.MQTTv311)

azureClient.on_connect = on_connect
azureClient.on_disconnect = on_disconnect
azureClient.on_publish = on_publish
azureClient.on_message = on_message
azureClient.on_subscribe = on_subscribe
azureClient.on_unsubscribe = on_unsubscribe

azureClient.username_pw_set(username=iot_hub_name+".azure-devices.net/" +
                       device_id + "/?api-version=2018-06-30", password=sas_token)

azureClient.tls_set(ca_certs=path_to_root_cert, certfile=None, keyfile=None,
                                                  cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
azureClient.tls_insecure_set(False)

azureClient.connect(iot_hub_name+".azure-devices.net", port=8883)
azureClient.subscribe(("#", 1))
azureClient.loop_start()
while True:
    try:
        sleep(1)
        IoTmsg = '{voltage=' + str(randint(0,10)) + '}'
        azureClient.publish("devices/" + device_id + "/messages/events/", IoTmsg, qos=1)
        

                
    except KeyboardInterrupt:
        azureClient.loop_stop()
        azureClient.disconnect()
        break
