import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)

p1 = GPIO.PWM(22,50)
p1.start(0)
p2 = GPIO.PWM(23,50)
p2.start(0)
p3 = GPIO.PWM(24,50)
p3.start(0)
p4 = GPIO.PWM(25,50)
p4.start(0)

dir = 1
rep = 0
start = 0
end = 100

while(rep <= 100):
    for dc in range(start, end, dir):
        p1.ChangeDutyCycle(dc)
        p2.ChangeDutyCycle(dc)
        p3.ChangeDutyCycle(dc)
        p4.ChangeDutyCycle(dc)
	time.sleep(0.01)
	rep = rep + 1
    print(rep)
    start = 100
    end = 0
    dir = -1
    time.sleep(0.2)

pos1 = [40, 20, 10, 5, 0, 0, 0, 0, 0, 0, 0, 0, 100, 100, 100, 50]
pos2 = [100, 50, 40, 20, 10, 5, 0, 0, 0, 0, 100, 50, 40, 40, 40, 50]
pos3 = [0, 100, 100, 50, 40, 40, 40, 50, 100, 50, 40, 20, 10, 5, 0, 0]
pos4 = [0, 0, 0, 100, 100, 100, 100, 50, 40, 20, 10, 5, 0, 0, 0, 0]
repeat = 0

while True:
    p1.ChangeDutyCycle(pos1[repeat])
    p2.ChangeDutyCycle(pos2[repeat])
    p3.ChangeDutyCycle(pos3[repeat])
    p4.ChangeDutyCycle(pos4[repeat])
    repeat = repeat + 1
    if(repeat == 16):
	repeat = 0
    time.sleep(0.1)

GPIO.cleanup()
