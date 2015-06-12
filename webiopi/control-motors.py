import webiopi
import time

webiopi.setDebug()

GPIO = webiopi.GPIO

# Valuables for GPIO Pin on Raspberry Pi
Pin1 = 17
Pin2 = 27
SERVO = 22

# Servo control valuable
DEFAULT_ANGLE = 0			# This constant needs to be replaced
CURRENT_ANGLE = DEFAULT_ANGLE
time_stamp = time.time()

# DC Motor control valuable
pulltime = 3
waittime = 2
releasetime = 3
PIN1 = None
PIN2 = None

def setup():
	GPIO.setFunction(SERVO, GPIO.PWM)
	GPIO.pulseAngle(SERVO, DEFAULT_ANGLE)
	webiopi.sleep(0.5)
	GPIO.pulseRatio(SERVO, 0)
	setpin(Pin1,Pin2)

def loop():
	global time_stamp
	if(time_stamp <= time.time() - 30):
		defaultPosition()

	webiopi.sleep(0.5)


# ----------  Servo Control Functions  --------------#
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
def graduateLeft():
	global CURRENT_ANGLE, time_stamp
	webiopi.debug("graduateleft")
	if CURRENT_ANGLE < DEFAULT_ANGLE and time_stamp <= time.time() - 0.2:
		for i in range(0,30):
			GPIO.pulseRatio(SERVO, 1)
			time_stamp = time.time()
			CURRENT_ANGLE = CURRENT_ANGLE + 1
			GPIO.pulseAngle(SERVO, CURRENT_ANGLE)
			webiopi.sleep(0.015)
			GPIO.pulseRatio(SERVO, 0)
		time_stamp = time.time()

@webiopi.macro
def graduateRight():
	global CURRENT_ANGLE, time_stamp
	webiopi.debug("graduateright")
	if CURRENT_ANGLE > DEFAULT_ANGLE - 9*10 and time_stamp <= time.time() - 0.2:
		for i in range(0,30):
			GPIO.pulseRatio(SERVO, 1)
			time_stamp = time.time()
			CURRENT_ANGLE = CURRENT_ANGLE - 1
			GPIO.pulseAngle(SERVO, CURRENT_ANGLE)
			webiopi.sleep(0.015)
			GPIO.pulseRatio(SERVO, 0)
		time_stamp = time.time()

@webiopi.macro
def left():
	global CURRENT_ANGLE,time_stamp
	webiopi.debug("left")
	if CURRENT_ANGLE < DEFAULT_ANGLE and time_stamp <= time.time() - 0.2:
		GPIO.pulseRatio(SERVO, 1)
		time_stamp = time.time()
		CURRENT_ANGLE = CURRENT_ANGLE + 30
		GPIO.pulseAngle(SERVO, CURRENT_ANGLE)
		webiopi.sleep(0.5)
		time_stamp = time.time()
		GPIO.pulseRatio(SERVO, 0)

@webiopi.macro
def right():
	global CURRENT_ANGLE, time_stamp
	webiopi.debug("right")
	if CURRENT_ANGLE > DEFAULT_ANGLE - 9*10 and time_stamp <= time.time() - 0.2:
		GPIO.pulseRatio(SERVO, 1)
		time_stamp = time.time()
		CURRENT_ANGLE = CURRENT_ANGLE - 30
		GPIO.pulseAngle(SERVO, CURRENT_ANGLE)
		webiopi.sleep(0.5)
		time_stamp = time.time()
		GPIO.pulseRatio(SERVO, 0)


# -----------  DC Motor Control Functions  -------------- #
@webiopi.macro
def fireExtinguish():
    webiopi.debug("fireExtinguish")
    webiopi.debug("FireFight!")
    positive_rotation()
    webiopi.debug("Pulling")
    webiopi.sleep(pulltime)
    stop()
    webiopi.debug("Waiting")
    webiopi.sleep(waittime)
    negative_rotation()
    webiopi.debug("Releasing")
    webiopi.sleep(releasetime)
    webiopi.debug("Finished")
    stop()
    webiopi.sleep(2)

@webiopi.macro
def wireRelease():
	webiopi.debug("wireRelease")
	negative_rotation()
	webiopi.sleep(releasetime)
	stop()
	webiopi.sleep(2)


def setpin(Pin1, Pin2) :
# 引数で受け取ったピン番号を出力端子として設定
    global PIN1,PIN2
        # GPIOの初期化
        # GPIO.setmode(GPIO.BCM)
    GPIO.setFunction(Pin1, GPIO.OUT);	PIN1 = Pin1
    GPIO.setFunction(Pin2, GPIO.OUT);	PIN2 = Pin2

def positive_rotation() :
# モーターを正回転させる
    if(PIN1 and PIN2) :
        webiopi.debug("positive rotation")
        GPIO.digitalWrite(PIN1,True)
        GPIO.digitalWrite(PIN2,False)

def negative_rotation() :
# モーターを逆回転させる
    if(PIN1 and PIN2) :
        webiopi.debug("negative rotation")
        GPIO.digitalWrite(PIN1,False)
        GPIO.digitalWrite(PIN2,True)

def stop() :
# モーターの回転を止める
    if(PIN1 and PIN2) :
        GPIO.digitalWrite(PIN1,False)
        GPIO.digitalWrite(PIN2,False)


def destroy():
	GPIO.setup(SERVO, GPIO.IN)
	