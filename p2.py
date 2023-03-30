from gpiozero import Button
from time import sleep

clk = Button(6)					#setting clock to gpio 6
dt =  Button(5)					#setting data to gpio 5
sw =  Button(27, pull_up=True)			#setting button to gpio 27

def rotation():					#defining rotation if data is on it prints ccw and vise versa
        if dt.value == 1:
                print("counter-clockwise")
        else:
                print("clockwise")

clk.when_pressed = rotation			#when pressed/ rotated it will print

def press():					#defining button when pressed
	if sw.value == 1:
		print("pressed")

sw.when_pressed = press

while True:					#passing to while loop to keep function runnning
        pass
