from __future__ import division
from Tkinter import *
import time
import math

# ---- Global objects ----
root = Tk()

cBcX = 20							# Center Base centerX
cBcY = 300							# Center Base centerY
circleBaseCenter = (cBcX, cBcY)
lengthBase = 108*1.5
lengthArm = 110*1.5

# Import the PCA9685 module.
import Adafruit_PCA9685
pwm = Adafruit_PCA9685.PCA9685()

# Configure min and max servo pulse lengths
servo_min = 150  #Min pulse length out of 4096
servo_max = 650  # Max pulse length out of 4096

# Helper function to make setting a servo pulse width simpler.
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

def move_base_servo(angleBaseDeg):
    pwm_pulse = int((servo_max-servo_min)/180*angleBaseDeg+servo_min)
    pwm.set_pwm(0, 0, pwm_pulse)
    print("moving Robot base to: pwm " + str(pwm_pulse))
    time.sleep(0.1)

def move_arm_servo(angleArmDeg):
    pwm_pulse = int((servo_min-servo_max)/180*angleArmDeg+servo_max)
    pwm.set_pwm(1, 0, pwm_pulse)
    print("moving Robot arm to: pwm " + str(pwm_pulse))
    time.sleep(0.1)

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)

# ---- Classes ------
def sliderActivate(GUI):
    GUI.getSliderValues()

class startGUI:
    def __init__(self, master):
        self.master = master
        self.canvas = Canvas(master, width=400, height=600)
        self.canvas.pack(side=LEFT)
        
        self.angleBaseDeg = 90
        self.angleArmDeg = 90
        self.angleBase = math.radians(self.angleBaseDeg)
        self.angleArm = math.radians(self.angleArmDeg)

        self.mX = 0
        self.mY = 0
        self.drawModeBoolean = False
        self.robotModeBoolean = False
        self.graphics = []
        self.lastClick = []

        self.buttonCanvas = Canvas(master, width=100, height=600)
        self.buttonCanvas.pack(side=TOP)

        self.raiseButton = Button(self.buttonCanvas, text="Raise (+)", command= lambda: raiseFunction())
        self.raiseButton.grid(row=0, column=0)
        self.lowerButton = Button(self.buttonCanvas, text="Lower (-)", command= lambda: lowerFunction())
        self.lowerButton.grid(row=1, column=0)
        self.displayHelpButtonBG = "gray86"
        self.displayBoolean = False
        self.displayHelpButton = Button(self.buttonCanvas, text="Help lines", background=self.displayHelpButtonBG, command= lambda: self.displayHelpLines())        
        self.displayHelpButton.grid(row=4, column=0)
        self.drawModeButtonBG = "gray86"
        self.drawModeButton = Button(self.buttonCanvas, text="Draw", background=self.drawModeButtonBG, command= lambda: self.drawMode())        
        self.drawModeButton.grid(row=5, column=0)
        self.robotModeButtonBG = "gray86"
        self.robotModeButton = Button(self.buttonCanvas, text="Robot", background=self.robotModeButtonBG, command= lambda: self.robotMode())        
        self.robotModeButton.grid(row=6, column=0)
        self.lineSlider = Scale(self.buttonCanvas, from_=0, to=180, command= lambda x: self.getSliderValues())
        self.lineSlider.set(self.angleBaseDeg)
        self.lineSlider.grid(row=2, column=0)
        self.lineSliderArm = Scale(self.buttonCanvas, from_=0, to=180, command= lambda x: self.getSliderValues())
        self.lineSliderArm.set(self.angleArmDeg)
        self.lineSliderArm.grid(row=3, column=0)

        self.cAcX = self.cAcY = self.X_bt = self.Y_bt = self.X_bb = self.Y_bb = self.X_at = self.Y_at = self.X_ab = self.Y_ab = self.X_at2 = self.Y_at2 = self.X_ab2 = self.Y_ab2 = self.cPcX = self.cPcY = self.X_pt = self.Y_pt = self.X_pb = self.Y_pb = None

        self.canvas.bind("<Button-1>", self.mouseCallback)
        
    def getSliderValues(self):
        update = False
        if (self.lineSlider.get() != self.angleBaseDeg or self.lineSliderArm.get() != self.angleArmDeg): #and Manual enabled
            self.updateGUIAngles(self.lineSlider.get(), self.lineSliderArm.get())
            update = True
        if (update):
            self.updateShapes()
            self.draw()
    def mouseCallback(self, event):
        print("clicked at x: " + str(event.x) + " y: " + str(event.y))
        self.moveToXY(event.x, event.y)
        #if(self.drawModeBoolean):
        #    self.graphics.append([event.x, event.y])
        #else:
        #    self.graphics.append(0)
        
        #if(not self.drawModeBoolean and len(self.graphics) != 0):
        #    if(self.graphics[-1] != 0):
        #        self.graphics.append(0)
        if(self.drawModeBoolean):
            if(len(self.lastClick) != 0):
                self.graphics.append(self.lastClick)
            self.graphics.append([event.x, event.y])
        self.lastClick = [event.x, event.y]
        print(self.graphics)
        self.draw()

        #self.pathToXY(event.x, event.y)

    def mousePosition(self, event):
        self.mX = event.x
        self.mY = event.y
        
        #print("mX = " + str(self.mX) + " mY = " + str(self.mY))

    def pathToXY(self, newX, newY):
        startX = self.cPcX
        startY = self.cPcY
        print("Start X = " + str(startX) + " Start Y = " + str(startY))
        distance = math.sqrt((newY - startY)**2 + (newX - startX)**2)
        alpha = math.atan((newX - startX)/(newY - startY))
        dx = 1.00*math.sin(alpha)
        dy = 1.00*math.cos(alpha)
        print("alpha = " + str(alpha) + " dx = " + str(dx) + " dy = " + str(dy))
        X = startX + dx
        Y = startY + dy
        print("move to X = " + str(X) + " move to Y Y = " + str(Y))
        print("move to (int) X = " + str(int(round(X))) + " move to (int) Y = " + str(int(round(Y))))
        while(int(round(X)) != newX or int(round(Y)) != newY):
            self.moveToXY(int(round(X)), int(round(Y)))
            X += dx
            Y += dy
            #self.moveToXY(int(round(X)), int(round(Y)))
            print("new X = " + str(X) + " new Y = " + str(Y))
            print("new X (int) = " + str(int(round(X))) + " new Y = " + str(int(round(Y))))
            time.sleep(0.05)

    def moveToXY(self, newX, newY):
        newX -= cBcX
        newY -= cBcY
        newY *= -1
        startX = self.cPcX - cBcX
        startY = -1*(self.cPcY - cBcY)
        distance_path = math.sqrt((newY - startY)**2 + (newX - startX)**2)
        alpha = math.atan((newX - startX)/(newY - startY))
        dx = 1.00*math.sin(alpha)
        dy = 1.00*math.cos(alpha)
        X = startX + dx
        Y = startY + dy
        continueBoolean = True
        while(int(round(X)) != newX or int(round(Y)) != newY and continueBoolean):
            if(not(self.drawModeBoolean)):
                continueBoolean = False
                X = newX
                Y = newY
                
            dist = float(math.sqrt(X**2 + Y**2))
            angleBaseDummy = float(180/math.pi*math.asin(math.sin(math.acos((float(lengthBase)**2-dist**2+float(lengthArm)**2)/(2*lengthBase*lengthArm)))*float(lengthArm)/dist) + 180/math.pi*math.atan(newY/newX))
            #angleBaseDummy = float(180/math.pi*math.acos((lengthBase**2+dist**2-lengthArm**2)/(2*lengthBase*dist)) + 180/math.pi*math.atan(newY/newX))
            angleArmDummy = float(180/math.pi*math.acos((float(lengthBase)**2-dist**2+float(lengthArm)**2)/(2*lengthBase*lengthArm)))
            #angleArmDummy = float(180/math.pi*math.acos((lengthBase**2-dist**2+lengthArm**2)/(2*lengthBase*dist)))
            print("angleBaseDummy = " + str(angleBaseDummy) + " angleArmDummy = " + str(angleArmDummy))
            if (angleBaseDummy > 90):
                angleBaseDummy = float(180/math.pi*(math.atan(float(newY)/float(newX))-math.asin(math.sin(math.pi/180*angleArmDummy)*float(lengthArm)*dist)))
                angleArmDummy = 360 - angleArmDummy
            if (angleBaseDummy >= 0):
                self.angleBaseDeg = int(angleBaseDummy + 0.5 + 90)
            if (angleArmDummy >= 90):
                #self.angleArmDeg = int(angleArmDummy + 0.5 - 90)
                self.angleArmDeg = int(270 - angleArmDummy + 0.5)
            if (angleBaseDummy < 0):
                #self.angleBaseDeg = int(90 - angleBaseDummy - 0.5)
                self.angleBaseDeg = int(90 + angleBaseDummy + 0.5)
            print("angleBase = " + str(self.angleBaseDeg) + " angleArm = " + str(self.angleArmDeg))
            self.updateGUIAngles(self.angleBaseDeg, self.angleArmDeg)
            self.updateShapes()
            self.draw()
            if (self.robotModeBoolean):
                    move_base_servo(self.angleBaseDeg)
                    print("moving Robot base to: angle " + str(self.angleBaseDeg))
                    move_arm_servo(self.angleArmDeg)
            X += dx
            Y += dy
                
            
    def displayHelpLines(self):
        if (not(self.displayBoolean)):
            self.displayHelpButtonBG = "CadetBlue1"
            self.displayHelpButton.config(background=self.displayHelpButtonBG)
            self.displayBoolean = True
        else:
            self.displayHelpButtonBG = "gray86"
            self.displayHelpButton.config(background=self.displayHelpButtonBG)
            self.displayBoolean = False
        self.draw()

    def drawMode(self):
       if (not(self.drawModeBoolean)):
           self.drawModeButtonBG = "CadetBlue1"
           self.drawModeButton.config(background=self.drawModeButtonBG)
           self.drawModeBoolean = True
       else:
           self.drawModeButtonBG = "gray86"
           self.drawModeButton.config(background=self.drawModeButtonBG)
           self.drawModeBoolean = False

    def robotMode(self):
       if (not(self.robotModeBoolean)):
           self.robotModeButtonBG = "CadetBlue1"
           self.robotModeButton.config(background=self.robotModeButtonBG)
           self.robotModeBoolean = True
       else:
           self.robotModeButtonBG = "gray86"
           self.robotModeButton.config(background=self.robotModeButtonBG)
           self.robotModeBoolean = False

    def updateGUIAngles(self, angleBaseDeg, angleArmDeg):
        self.angleBaseDeg = angleBaseDeg
        self.angleArmDeg = angleArmDeg
        self.angleBase = math.radians(self.angleBaseDeg)
        self.angleArm = math.radians(self.angleArmDeg)

    def updateShapes(self):
        self.cAcX = int(round(cBcX + lengthBase*math.sin(self.angleBase)))        # Center Arm centerX
        self.cAcY = int(round(cBcY + lengthBase*math.cos(self.angleBase)))        # Center Arm centerY

        self.X_bt = int(round(cBcX + 10*math.cos(self.angleBase)))		# X for base top edge
        self.Y_bt = int(round(cBcY - 10*math.sin(self.angleBase)))		
        self.X_bb = int(round(cBcX - 10*math.cos(self.angleBase)))		# X for base bottom edge
        self.Y_bb = int(round(cBcY + 10*math.sin(self.angleBase)))

        self.X_at = int(round(self.cAcX + 10*math.cos(self.angleBase)))                # X for base top edge
        self.Y_at = int(round(self.cAcY - 10*math.sin(self.angleBase)))
        self.X_ab = int(round(self.cAcX - 10*math.cos(self.angleBase)))                # X for base bottom edge
        self.Y_ab = int(round(self.cAcY + 10*math.sin(self.angleBase)))

        self.X_at2 = int(round(self.cAcX + 10*math.sin(self.angleArm - self.angleBase)))
        self.Y_at2 = int(round(self.cAcY - 10*math.cos(self.angleArm - self.angleBase)))
        self.X_ab2 = int(round(self.cAcX - 10*math.sin(self.angleArm - self.angleBase)))
        self.Y_ab2 = int(round(self.cAcY + 10*math.cos(self.angleArm - self.angleBase)))

        self.cPcX = int(round(self.cAcX + lengthArm*math.cos(self.angleArm - self.angleBase)))
        self.cPcY = int(round(self.cAcY + lengthArm*math.sin(self.angleArm - self.angleBase)))

        self.X_pt = int(round(self.cPcX + 10*math.sin(self.angleArm - self.angleBase)))
        self.Y_pt = int(round(self.cPcY - 10*math.cos(self.angleArm - self.angleBase)))
        self.X_pb = int(round(self.cPcX - 10*math.sin(self.angleArm - self.angleBase)))
        self.Y_pb = int(round(self.cPcY + 10*math.cos(self.angleArm - self.angleBase)))

    def draw(self):
        self.canvas.delete("all")
        if(self.displayBoolean):
            self.displayLineOuter = self.canvas.create_arc(cBcX-lengthBase-lengthArm, cBcY-lengthBase-lengthArm, cBcX+lengthBase+lengthArm, cBcY+lengthBase+lengthArm, start=-90, extent=180, outline="black")
            self.displayLineInner = self.canvas.create_arc(cBcX-int(math.sqrt(lengthBase**2+lengthArm**2)), cBcY-int(math.sqrt(lengthBase**2+lengthArm**2)), cBcX+int(math.sqrt(lengthBase**2+lengthArm**2)), cBcY+int(math.sqrt(lengthBase**2+lengthArm**2)), start=-90, extent=180, outline="black")
        i = 0
        while(i < len(self.graphics)):
            #self.drawingline = self.canvas.create_line(self.graphics[i][0], self.graphics[i][1], self.graphics[i+1][0], self.graphics[i+1][1])
            self.drawingline = self.canvas.create_line(self.graphics[i], self.graphics[i+1])
            i += 2
            
        self.polygonBaseCoord = [self.X_bt, self.Y_bt, self.X_at, self.Y_at, self.X_ab, self.Y_ab, self.X_bb, self.Y_bb]
        self.polygonBase = self.canvas.create_polygon(self.polygonBaseCoord, outline="black", fill="grey")
        self.polygonArmCoord = [self.X_at2, self.Y_at2, self.X_pt, self.Y_pt, self.X_pb, self.Y_pb, self.X_ab2, self.Y_ab2]
        self.polygonArm = self.canvas.create_polygon(self.polygonArmCoord, outline="black", fill="grey")
        self.circleBase = self.canvas.create_oval(circleBaseCenter[0]-10, circleBaseCenter[1]-10, circleBaseCenter[0]+10, circleBaseCenter[1]+10, outline="black", fill="DarkOrange1")
        self.circleArm = self.canvas.create_oval(self.cAcX-10, self.cAcY-10, self.cAcX+10, self.cAcY+10, outline="black", fill="DarkOrange1")
        self.circlePen = self.canvas.create_oval(self.cPcX-10, self.cPcY-10, self.cPcX+10, self.cPcY+10, outline="black")#, fill="DarkOrange")


GUI = startGUI(root)
GUI.updateShapes()
GUI.draw()
root.bind('<Motion>', GUI.mousePosition)
root.mainloop()
