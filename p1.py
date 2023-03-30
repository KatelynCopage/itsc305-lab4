from gpiozero import Button
from time import sleep

clk = Button(6)
dt =  Button(5)
sw =  Button(27, pull_up=True)

def rotation():
	if dt.value == 1:
		print("counter-clockwise")
	else:
		print("clockwise")

clk.when_pressed = rotation

while True:
	pass
