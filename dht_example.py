import RPi.GPIO as GPIO
import DHT as dht11
from time import sleep

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# read data using pin 14
instance = dht11.DHT11(pin=12)
result = instance.read()
#sleep(2)

if result.is_valid():
    print("Temperature: %-3.1f C" % result.temperature)
    print("Humidity: %-3.1f %%" % result.humidity)
else:
    print("Error: %d" % result.error_code)

GPIO.cleanup()
