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
print('display: ' + "".join(display))
def DisplayScroll(display):
	k=0
	j=0
	while True:
		if display[k]==' ' and k<=14:
			k += 1
		else:
			pos = k
			print("k= " + str(k))
			while j<k:
				lcd.clear()
				scrollDisp = display[:]
				print("Display= " + "".join(display))
				scrollDisp[j]= 'O'
				lcd.message("".join(scrollDisp))
				print("K====: " + "".join(scrollDisp))
				time.sleep(0.1)
				j += 1
			return;
	
def DisplayInput(display):
	i = 0
	while i<=15:
		if display[i] == ' ' and i <= 14:
			print('i= ' + str(i))
			i += 1
		elif i==15 and display[i]==' ':
			print("i==15 och i:" + str(i))
			display[i]='O'
			i += 1
		else:
			print("i<15 och i:" + str(i))
			nr = i-1
			display[nr]='O'
			i += 1 
	return display;
while True:
	enter = raw_input("Enter: ")
	if enter == "e":
		lcd.clear()
		DisplayScroll(display)
		lcd.message("".join(DisplayInput(display)))
		time.sleep(1.0)
#for k in range (0, 15):
#	lcd.clear()
#	message = " ".join([str(x) for x in DisplayInput(display)])
#	print('message: ' + message)
#	lcd.message(message)
#	time.sleep(1.0)

#for i in range(lcd_columns-len('O')):
#	time.sleep(0.25)
#	lcd.move_right()
#
#lcd.message('1')
#for i in range(lcd_columns-2):
#	time.sleep(0.25)
#	lcd.move_right()
