import RPi.GPIO as GPIO
from gpiozero import Button
import sonic								#import distance
import DHT
import driver as lcd_d
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


#global variables
menu_selection = 0
button_selection = 0

#setting distance
distance = sonic.distance()
trig = 26	#sending trigger to gpio 26
echo = 19	#sending trigger to gpio 19

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#initialize display
display = lcd_d.lcd()

# read data using pin 12
instance = DHT.DHT11(pin=12)
result = instance.read()

#setting rotary encoder gpios
clk = Button(16)
dt = Button(20)
sw = Button(21, pull_up=True)

def on_connect(client, userdata, flags, rc):
    print("Connected ", rc)

def on_publish(client, userdata, result):
	print("Published ", result)

def on_log(client, userdata, level, buf):
	print("log: ", buf)

#incrementing rotation back and forth (cw and ccw) and looping them so they are continuous
def rotation():

	global menu_selection		#calling menu selection
	if dt.value == 0:		#setting data to 0
		if menu_selection == 2:
			menu_selection = 0
		else:
			menu_selection = menu_selection + 1	#incrementing rotation
	else:

		if menu_selection == 0:
			menu_selection = 2
		else:
			menu_selection = menu_selection - 1	#decrementing rotation
	main_menu_change(menu_selection)
#	press(menu_selection)

#defining the press function to display when it is on a certain function
def press():
	global menu_selection			#calling menu selection
	if menu_selection  == 2:		#calling menu selection = to distance as in the menu change function
		display.lcd_display_string(("Distance:          "), 1)
		display.lcd_display_string((" %.1fcm             " % distance), 2)
		sleep(5)
		main_menu_change(menu_selection)
	elif menu_selection == 0:		#calling menu selection = to 0 in the temp as in the change function
		display.lcd_display_string(("Temperature:          "), 1)
		display.lcd_display_string((" %-3.1f C             " % result.temperature), 2)
		sleep(5)
		main_menu_change(menu_selection)
	elif menu_selection == 1:		#setting menu selection = to 1 in humidity in the chnage function
		display.lcd_display_string(("Humidity:          "), 1)
		display.lcd_display_string((" %-3.1f %%             " % result.humidity), 2)
		sleep(5)
		main_menu_change(menu_selection)

#Setting up menu when it changes to different temperture, humidity, and distance
def main_menu_change(selection):
	display.lcd_display_string("Main Menu:                 ", 1, 0)
	if selection == 0:
		display.lcd_display_string("Temperature        ", 2, 0)
	elif selection == 1:
		display.lcd_display_string("Humidity           ", 2, 0)
	elif selection == 2:
		display.lcd_display_string("Distance           ", 2, 0)

#When pressed clock will go into the rotation function
clk.when_pressed = rotation
#When pressed switch will go into the press function
sw.when_pressed = press

#Passing a while loop to keep the program running
try:
	client = mqtt.Client(client_id=MQTT_CLIENT_ID, clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")
	client.on_connect = on_connect
	client.on_publish = on_publish
	client.username_pw_set(MQTT_USERNAME, password=MQTT_PASSWD)
	client.connect(MQTT_HOST, port=MQTT_PORT, keepalive=60)
	client.loop_start()
	while True:
		sleep(1)
		if not client.is_connected:
			print("Client disconnected. Trying to reconnect.")
			client.reconnect()
		pub_topic = "field1=" + str(randint(0, 500)/100) #publish random number between 0.00 and 4.99 to Field 5 of ThingSpeak Channel
		client.publish(MQTT_PUBLISH_TOPIC, pub_topic)


#GPIO.cleanup()
except KeyboardInterrupt:
	print("Cleaning up")
	display.lcd_clear
