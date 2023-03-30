from time import sleep
import paho.mqtt.client as mqtt
from random import randint

MQTT_CLIENT_ID = "ITSC305" # This is for your own client identification. Can be anything
MQTT_USERNAME = "mwa0000024762006" #This is the ThingsSpeak's Author
MQTT_PASSWD = "QV64LNWEZNLJ4AR0" #This is the MQTT API Key found under My Profile in ThingSpeak
MQTT_HOST = "mqtt.thingspeak.com" #This is the ThingSpeak hostname
MQTT_PORT = 1883 #Typical port # for MQTT protocol. If using TLS -> 8883
CHANNEL_ID = "1574862" #Channel ID found on ThingSpeak website
MQTT_WRITE_APIKEY = "RCHNFZL87Q8UHFAU" # Write API Key found under ThingSpeak Channel Settings
MQTT_PUBLISH_TOPIC = "channels/" + CHANNEL_ID + "/publish/" + MQTT_WRITE_APIKEY

""" 
Standard callback functions. See Phao MQTT documentation for more

This function will be called upon connection
"""

def on_connect(client, userdata, flags, rc):
    print("Connected ", rc)

"""
This function is called upon Publishing of data to predefined topic
"""

def on_publish(client, userdata, result):
    print("Published ", result)

""" 
This function is used for logging. For this to work, you must uncomment the callback binding
"""
def on_log(client, userdata, level, buf):
    print("log:", buf)


try:
    """ create client instance"""
    client = mqtt.Client(client_id=MQTT_CLIENT_ID, clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")

    """ standard callback bindings """

    client.on_connect = on_connect
    #client.on_message = on_message
    #client.on_subscribe = on_subscribe
    #client.on_unsubscribe = on_unsubscribe
    #client.on_disconnect = on_disconnect
    client.on_publish = on_publish
    #client.on_log = on_log

    """ Set the conneciton authentication. """
    client.username_pw_set(MQTT_USERNAME, password=MQTT_PASSWD)
    """ Connect client """
    client.connect(MQTT_HOST, port=MQTT_PORT, keepalive=60)
    """ start the looping of client connection. This needs to be done otherwise the connection will only happen once and expire """
    client.loop_start()

    while True:
       sleep(1)
       if not client.is_connected:
            print("Client disconnected. Trying to reconnect.")
            client.reconnect()
       pub_topic = "field5=" + str(randint(0, 500)/100) #publish random number between 0.00 and 4.99 to Field 5 of ThingSpeak Channel
       client.publish(MQTT_PUBLISH_TOPIC, pub_topic)

except KeyboardInterrupt:
    client.disconnect()
