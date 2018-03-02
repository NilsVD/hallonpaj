from Tkinter import *
import time
import math

i = 0
root = Tk()

canvas = Canvas(root, width=400, height=600)
canvas.pack(side=LEFT)

buttonCanvas = Canvas(root, width=100, height=600)
buttonCanvas.pack(side=TOP)
cBcX = 20							# Center Base centerX
cBcY = 300							# Center Base centerY
circleBaseCenter = (cBcX, cBcY)
lengthBase = 106
lengthArm = 164
angleBaseDeg = 90
angleArmDeg = 90
angleBase = math.radians(angleBaseDeg)
angleArm = math.radians(angleArmDeg)

#blackLine = canvas.create_line(0, 0, 200, 50) 	#(StartxX, startY, endX, end
#greenBox = canvas.create_rectangle(25, 25, 130, 60, fill="green")	#StartXcorner, startYcorner, endXcorner, endYcorner
#i = 0

raiseButton = Button(buttonCanvas, text="Raise (+)", command= lambda: raiseFunction())
raiseButton.grid(row=0, column=0)
lowerButton = Button(buttonCanvas, text="Lower (-)", command= lambda: lowerFunction())
lowerButton.grid(row=1, column=0)
lineSlider = Scale(buttonCanvas, from_=0, to=180)
lineSlider.set(angleBaseDeg)
lineSlider.grid(row=2, column=0)
lineSliderArm = Scale(buttonCanvas, from_=0, to=180)
lineSliderArm.set(angleArmDeg)
lineSliderArm.grid(row=3, column=0)

def updateShapes():
	global cAcX, cAcY, cPcX, cPcY, X_bt, Y_bt, X_bb, Y_bb, X_at, Y_at, X_ab, Y_ab, X_at2, Y_at2, X_ab2, Y_ab2, X_pt, Y_pt, X_pb, Y_pb

	cAcX = int(round(cBcX + lengthBase*math.sin(angleBase)))        # Center Arm centerX
	cAcY = int(round(cBcY + lengthBase*math.cos(angleBase)))        # Center Arm centerY

	X_bt = int(round(cBcX + 10*math.cos(angleBase)))		# X for base top edge
	Y_bt = int(round(cBcY - 10*math.sin(angleBase)))		
	X_bb = int(round(cBcX - 10*math.cos(angleBase)))		# X for base bottom edge
	Y_bb = int(round(cBcY + 10*math.sin(angleBase)))

	X_at = int(round(cAcX + 10*math.cos(angleBase)))                # X for base top edge
	Y_at = int(round(cAcY - 10*math.sin(angleBase)))
	X_ab = int(round(cAcX - 10*math.cos(angleBase)))                # X for base bottom edge
	Y_ab = int(round(cAcY + 10*math.sin(angleBase)))

	X_at2 = int(round(cAcX + 10*math.sin(angleArm - angleBase)))
	Y_at2 = int(round(cAcY - 10*math.cos(angleArm - angleBase)))
	X_ab2 = int(round(cAcX - 10*math.sin(angleArm - angleBase)))
	Y_ab2 = int(round(cAcY + 10*math.cos(angleArm - angleBase)))

	cPcX = int(round(cAcX + lengthArm*math.cos(angleArm - angleBase)))
	cPcY = int(round(cAcY + lengthArm*math.sin(angleArm - angleBase)))

	X_pt = int(round(cPcX + 10*math.sin(angleArm - angleBase)))
        Y_pt = int(round(cPcY - 10*math.cos(angleArm - angleBase)))
        X_pb = int(round(cPcX - 10*math.sin(angleArm - angleBase)))
        Y_pb = int(round(cPcY + 10*math.cos(angleArm - angleBase)))

def moveToXY(newX, newY):
	global angleBaseDeg, angleArmDeg
	dist = math.sqrt(math.pow(newX, 2) + math.pow(newY, 2))
	angleBaseDummy = 180/math.pi*math.acos((math.pow(lengthBase, 2)+math.pow(dist, 2)-math.pow(lengthArm, 2))/(2*lengthBase*dist)) + 180/math.pi*math.atan(newY/newX)
	angleArmDummy = 180/math.pi*math.acos((math.pow(lengthBase, 2)-math.pow(dist, 2)+math.pow(lengthArm, 2))/(2*lengthBase*dist))
	if (angleBaseDummy > 90):
		angleBaseDummy = 180/math.pi*(math.atan(newy/newX)-math.asin(math.sin(math.pi/180*angleArmDummy)*lengthArm*dist))
		angleArmDummy = 360 - angleArmDummy
	## Fortsatt har	
	
	
def raiseFunction():
	global angleBaseDeg
	if (angleBaseDeg == 0):
		print("Raise but angleBase = 0")
		angleBaseDeg = 0
	else:
		print("Raise and i++")
		angleBaseDeg = angleBaseDeg - 1
		lineSlider.set(angleBaseDeg)
	print("angleBase = " + str(angleBaseDeg))

def lowerFunction():
	global angleBaseDeg
	if (angleBaseDeg == 180):
		angleBaseDeg = 180
	else:
		angleBaseDeg = angleBaseDeg + 1
		lineSlider.set(angleBaseDeg)
	print("angleBase = " + str(angleBaseDeg))

while (True):
	angleBaseDeg = lineSlider.get()
	angleBase = math.radians(angleBaseDeg)
	angleArmDeg = lineSliderArm.get()
	angleArm = math.radians(angleArmDeg)
	updateShapes()
	polygonBaseCoord = [X_bt, Y_bt, X_at, Y_at, X_ab, Y_ab, X_bb, Y_bb]
	polygonBase = canvas.create_polygon(polygonBaseCoord, outline="black", fill="grey")
	polygonArmCoord = [X_at2, Y_at2, X_pt, Y_pt, X_pb, Y_pb, X_ab2, Y_ab2]
        polygonArm = canvas.create_polygon(polygonArmCoord, outline="black", fill="grey")
	circleBase = canvas.create_oval(circleBaseCenter[0]-10, circleBaseCenter[1]-10, circleBaseCenter[0]+10, circleBaseCenter[1]+10, outline="black", fill="DarkOrange1")
	circleArm = canvas.create_oval(cAcX-10, cAcY-10, cAcX+10, cAcY+10, outline="black", fill="DarkOrange1")
	circlePen = canvas.create_oval(cPcX-10, cPcY-10, cPcX+10, cPcY+10, outline="black")#, fill="DarkOrange")
	root.update()
	time.sleep(0.1)
	canvas.delete(circleBase)
	canvas.delete(polygonBase)
	canvas.delete(circleArm)
	canvas.delete(polygonArm)
	canvas.delete(circlePen)
	root.update()
	#i += 1

root.mainloop()
