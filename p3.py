import subprocess

subprocess.run(["i2cset", "-y", "1", "0x27", "0x08"]) #running to address and command

while True:
	pass
