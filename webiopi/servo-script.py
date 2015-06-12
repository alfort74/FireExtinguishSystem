import webiopi
import time

GPIO = webiopi.GPIO
SERVO = 22
DEFAULT_ANGLE = -10			# This constant needs to be replaced
CURRENT_ANGLE = DEFAULT_ANGLE

time_stamp = time.time()

# def setup():
GPIO.setFunction(SERVO, GPIO.PWM)

GPIO.pulseAngle(SERVO, DEFAULT_ANGLE)
webiopi.sleep(0.5)
GPIO.pulseRatio(SERVO, 0)

def loop():
	global time_stamp
	if(time_stamp <= time.time() - 30):
		defaultPosition()

	webiopi.sleep(0.5)

@webiopi.macro
def defaultPosition():
	global time_stamp
	if time_stamp <= time.time() - 0.2 and (CURRENT_ANGLE != DEFAULT_ANGLE):
		time_stamp = time.time()
		global CURRENT_ANGLE
		CURRENT_ANGLE = DEFAULT_ANGLE
		GPIO.pulseRatio(SERVO, 1)
		GPIO.pulseAngle(SERVO,DEFAULT_ANGLE)
		webiopi.sleep(0.5)
		GPIO.pulseRatio(SERVO, 0)

@webiopi.macro
def left():
	global CURRENT_ANGLE,time_stamp
	webiopi.debug("left")
	if CURRENT_ANGLE < DEFAULT_ANGLE + 5*10 and time_stamp <= time.time() - 0.2:
		GPIO.pulseRatio(SERVO, 1)
		time_stamp = time.time()
		CURRENT_ANGLE = CURRENT_ANGLE + 5
		GPIO.pulseAngle(SERVO, CURRENT_ANGLE)
		webiopi.sleep(0.5)
		time_stamp = time.time()
		GPIO.pulseRatio(SERVO, 0)

@webiopi.macro
def right():
	global CURRENT_ANGLE, time_stamp
	webiopi.debug("right")
	if CURRENT_ANGLE > DEFAULT_ANGLE - 5*10 and time_stamp <= time.time() - 0.2:
		GPIO.pulseRatio(SERVO, 1)
		time_stamp = time.time()
		CURRENT_ANGLE = CURRENT_ANGLE - 5
		GPIO.pulseAngle(SERVO, CURRENT_ANGLE)
		webiopi.sleep(0.5)
		time_stamp = time.time()
		GPIO.pulseRatio(SERVO, 0)

def destroy():
	GPIO.setup(SERVO, GPIO.IN)