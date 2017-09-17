#Game for 16x2 LCD display

import time
import Adafruit_CharLCD as LCD
from random import randint

lcd = LCD.Adafruit_CharLCDPlate()

#Custom characters:

#Settings:
lcd_columns = 16
lcd_rows = 2

lcd.clear()
RightO = 'O'
LeftO = '\nO'

def RandO():
	i = randint(0,1)
	if i == 0:
		return RightO;
	else:
		return LeftO;

def Scroll(disp):
	scrollDisp = ' ' + disp
	return scrollDisp;

disp = 'O'
bottom = 16
#while len(disp)<bottom:
#	lcd.clear()
#	disp = Scroll(disp)
#	lcd.message(disp)
#	time.sleep(1.0)
display = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
def DisplayInput(display):
	i = 0
	print(i)
	while True:
		if display[i] == ' ' and i <= 15:
			print('i= ' + str(i))
			i += 1
		else:
			print('else')
			display[i]='O'
	return display;
print('message: ' + DisplayInput(display))
for k in range (0, 15):
	lcd.clear()
	message = " ".join([str(x) for x in DisplayInput(display)])
	print('message: ' + message)
	lcd.message(message)
	time.sleep(1.0)

#for i in range(lcd_columns-len('O')):
#	time.sleep(0.25)
#	lcd.move_right()
#
#lcd.message('1')
#for i in range(lcd_columns-2):
#	time.sleep(0.25)
#	lcd.move_right()
