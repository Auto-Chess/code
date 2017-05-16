import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)

GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

def light_coord(x, y):
    if y == 0:
        GPIO.output(20, 0)
        GPIO.output(21, 1)
    elif y==1:
        GPIO.output(20, 1)
        GPIO.output(21, 0)

    if x==0:
        GPIO.output(13, 1)
        GPIO.output(12, 0)
    elif x==1:
        GPIO.output(13, 0)
        GPIO.output(12, 1)



while True:
    try:
        """
        GPIO.output(13, 1)
        GPIO.output(12, 0)
        GPIO.output(20, 0)
        GPIO.output(21, 1)
        time.sleep(1)
        GPIO.output(13, 0)
        GPIO.output(12, 1)
        GPIO.output(20, 0)
        GPIO.output(21, 1)
        time.sleep(1)
        """
        light_coord(0, 0)
        time.sleep(1)
        light_coord(1, 0)
        time.sleep(1)
        light_coord(0, 1)
        time.sleep(1)
        light_coord(1, 1)
        time.sleep(1)
        """ 
        GPIO.output(12, 1)
        GPIO.output(13, 0)
        time.sleep(1)
        GPIO.output(12, 0)
        GPIO.output(13, 1)
        time.sleep(1)
        """   
    except KeyboardInterrupt as e:
        break;

GPIO.output(12, 0)
GPIO.output(13, 0)
GPIO.output(20, 0)
GPIO.output(21, 0)

GPIO.cleanup()
