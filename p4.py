import driver as lcd_d
display = lcd_d.lcd()
try:
	print("Writing to display")		#writes to display

	custom = [[0b00000,			#Creating Custom Characters through bitmapping
			0b00000,
			0b01010,
			0b00000,
			0b10001,
			0b01110,
			0b00000,
			0b00000],
						#Creates new list display
			[0b00000,
  			0b00000,
  			0b11011,
  			0b11111,
  			0b01110,
  			0b00100,
  			0b00000,
  			0b00000
		]]
	display.lcd_load_custom_chars(custom)	#loads the custom characters
	display.lcd_clear()			#clears it


	display.lcd_write(lcd_d.LCD_CURSORSHIFT) #shifts the display cursor
	display.lcd_write_char(0)		#writing custom characters

	display.lcd_display_string("", 1,10)	#passing an empty string to move the custom character
	display.lcd_write_char(0)
	display.lcd_display_string("", 2, 11)
	display.lcd_write_char(1)		#writing character
	display.lcd_display_string("Kyla", 1, 5) #Writing name to line 1, column 5
	display.lcd_display_string("Copage", 2, 4) #Writing last name to line 2 column

	while True:
		pass

except KeyboardInterrupt:			#keyboard interupt to clear display
	print("Cleaning up")
	display.lcd_clear
#mylcd = lcd_d.lcd()
#print("clear:")
#mylcd.lcd_clear()
#print("Hello")
#mylcd.lcd_display_string("Hello", 2)
